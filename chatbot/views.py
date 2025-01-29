from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db.models import Prefetch, Subquery, OuterRef
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Chats, Tags, Patterns, Responses  # Import relevant models
import json
from .chat_nlp import chatbot

from django.shortcuts import render


@method_decorator(csrf_exempt, name='dispatch')
# @method_decorator(login_required, name='dispatch')
class AskView(View):
    """
    Handles GET and POST requests for the 'ask/' endpoint.
    """

    def get(self, request):
        """
        Handle GET requests to fetch all chats.
        """
        try:
            chats = list(Chats.objects.values())  # Fetch all Chats as dictionaries
            return JsonResponse({'chats': chats}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        """
        Handle POST requests to process chatbot interactions.
        """
        try:
            # Parse the request body
            body = json.loads(request.body)

            quiz = str(body.get("name", "")).replace("?", "")


            # Prefetch related tags, patterns, and responses
            tags = Tags.objects.prefetch_related(
                Prefetch(
                    'patterns_set',
                    queryset=Patterns.objects.annotate(
                        pattern_name=Subquery(
                            Patterns.objects.filter(id=OuterRef('id')).values('name')
                        )
                    )
                ),
                Prefetch(
                    'responses_set',
                    queryset=Responses.objects.annotate(
                        response_name=Subquery(
                            Responses.objects.filter(id=OuterRef('id')).values('name')
                        )
                    )
                )
            )

            # Build intents from tags
            intents = {}
            for tag in tags:
                patterns = [pattern.name for pattern in tag.patterns_set.all()]
                responses = [response.name for response in tag.responses_set.all()]
                intents[tag.name] = {
                    'patterns': patterns,
                    'responses': responses,
                }

            # Pass the intents and quiz to the chatbot function

            print(intents)
            response = chatbot(intents, quiz)

            # Return the chatbot response
            return JsonResponse({'response': response}, status=201)

        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON payload.")
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




class EntryView(View):
    """
    Renders all initial chatbot entries
    """
    def get(self, request):
        return render(request, 'chatbot/health_queries.html')