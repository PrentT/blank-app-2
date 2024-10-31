import streamlit as st
import openai
import base64

# Streamlit App
st.title("Chat with GPT-4o")

# API Key input from user
api_key = st.text_input("Enter your OpenAI API key:", type="password")

# Text input from user
text_input = st.text_area("Enter your text prompt:")

# Image input from user
uploaded_image = st.file_uploader("Upload an image (optional):", type=["png", "jpg", "jpeg", "webp", "gif"])

# Button to submit the request
if st.button("Generate Response"):
    if api_key and text_input:
        # Set the API key
        openai.api_key = api_key

        # Prepare the message content
        message_content = [{"type": "text", "text": text_input}]
        
        # If image is uploaded, encode and add it
        if uploaded_image is not None:
            # Encode the image in base64
            base64_image = base64.b64encode(uploaded_image.read()).decode('utf-8')
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                    "detail": "auto"  # Using "auto" detail level for best performance
                }
            })
        
        # Make the API call
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": message_content}
                ],
                max_tokens=300
            )
            
            # Display the response
            st.success("Generated Response:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    elif not api_key:
        st.warning("Please provide your OpenAI API key.")
    else:
        st.warning("Please provide a text prompt to generate a response.")
