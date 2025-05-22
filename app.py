import os
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)
google_api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        response = model.generate_content(incoming_msg)
        bot_response = response.text
        msg.body(bot_response)
    except Exception as e:
        print(f"Erro ao chamar a Gemini API: {e}")
        msg.body("Desculpe, houve um erro ao processar sua mensagem.")

    return Response(str(resp), mimetype="application/xml")

if __name__ == '__main__':
    app.run(debug=False)
