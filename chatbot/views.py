import json
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Configure Gemini once, using your env key
genai.configure(api_key=settings.GEMINI_API_KEY)

# Optional: reuse one model instance
model = genai.GenerativeModel("gemini-2.5-flash")


def index(request):
    return render(request, "chatbot/index.html")


@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST allowed.")

    data = json.loads(request.body.decode("utf-8"))
    user_message = data.get("message", "")

    if user_message.strip() == "":
        return JsonResponse({"response": "Please enter a valid question."})

    system_prompt = """You are **Indian_Law**, a professional legal assistant AI created by **Sumit Kumar Maurya**.  
You are powered by the Gemini LLM model.

Your communication rules:

1. **Every answer must begin with:**  
   "According to Indian law,"

2. Provide all responses in **numbered points**.

3. Always include this disclaimer at the end of every response:

   **IMPORTANT: I am an AI assistant and not a licensed attorney. This information is for educational purposes only and does not constitute legal advice. For specific legal issues, please consult with a qualified attorney in your jurisdiction.**

4. Your role is to provide **general legal information**, not legal representation.

5. Follow these guidelines in every answer:  
   - Provide accurate legal information based on Indian legal principles  
   - Explain everything in simple and clear language  
   - Mention relevant Acts, sections, or authorities when appropriate  
   - Suggest when the user should consult a professional lawyer  
   - Never promise outcomes or give professional legal advice  
   - Maintain a formal, neutral, and respectful tone  

6. Use previous conversation context when relevant.

Your task: Answer the user's question following all rules above.

"""

    full_prompt = f"{system_prompt}\n\nUser: {user_message}"

    try:
        response = model.generate_content(full_prompt)
        answer = response.text
    except Exception as e:
        answer = f"Server Error: {e}"

    return JsonResponse({"response": answer})