import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
load_dotenv()
from PIL import Image
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input_prompt, image):
    #model = genai.GenerativeModel('gemini-flash-vision')
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text
def input_image_setup(uploaded_file):
    # check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                 "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded ")
st.set_page_config(page_title = "Calories Advisor App")

with st.sidebar:
    #image = Image.open('images/navbar.png')
    #st.image(image,width =200)
    selected = option_menu('Smart AI Nutrition Assistant',['Upload Your Meal','Generate Diet Plan'])
 
if(selected == 'Upload Your Meal'):
    # Initialize our streamlit app
    st.header("Calculate Calories using Image Ingredient Wise")
    uploaded_file = st.file_uploader("choose an image", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True )
    submit = st.button("Tell me about the total calories")
    input_prompt = """
    You are an expert in nutritionist where you need to see the food items from
    the image and calculate the total calories, also provide the details of 
    every food items with calories intake in below format
                1 Item 1 - no of calories
                2 Item 2 - no of calories
                -------
                ------
    finally you can also mention whether the food is healthy or not and also mention 
    the percentage split of the ration of carbohydrates, fats, fibers, sugar and 
    other important things required in our diet.
    """

    if submit:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_prompt, image_data)
        st.header("The Response is")
        st.write(response)
if(selected == 'Generate Diet Plan'):
    st.title("Personalized Nutrition Diet Plan Generator")

    # Create a layout with two columns to organize inputs, avoiding too much scrolling
    col1, col2 = st.columns(2)

    # Column 1 inputs
    with col1:
        # Input for age, with a minimum value of 1 year
        age = st.number_input("Age", min_value=1, step=1)
        # Input for height in feet, min 1 foot and max 8 feet
        height_feet = st.number_input("Height (Feet)", min_value=1, max_value=8, step=1)
        # Input for weight in kilograms, minimum value of 1.0 kg
        weight = st.number_input("Weight (kg)", min_value=1.0, step=0.1)
        # Select box for budget options (3 ranges represented by ₹ symbols)
        budget = st.text_input("Budget")

    # Column 2 inputs
    with col2:
        # Select box for choosing gender, with three options
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        # Input for height in inches, from 0 to 11 inches (complementing height in feet)
        height_inches = st.number_input("Height (Inches)", min_value=0, max_value=11, step=1)
        # Select box for choosing the type of diet, with various diet types available
        diet_type = st.selectbox("Diet Type", ["Vegetarian", "Vegan", "Keto", "Paleo", "Omnivore", "Other"])
        # Slider to select the number of unique meals per week (between 1 and 5)
        weekly_variety = st.slider("Number of unique meals per week", min_value=1, max_value=5, step=1)

    # Text area to input food dislikes or allergies, separated by commas
    dislikes = st.text_area("List any food dislikes or allergies (comma separated)")

    # Button to submit the user's input and generate the diet plan
    if st.button("Generate Diet Plan"):
        # Ensure all inputs have been provided
        if age and gender and weight and height_feet is not None and height_inches is not None and diet_type:
            # Display a loading spinner while the AI is generating the response
            with st.spinner("Generating your personalized diet plan..."):
                # Convert the user's height to total inches (feet * 12 + inches)
                total_height_inches = height_feet * 12 + height_inches
                
                # Mapping the selected display value to the actual text value for the prompt
                budget_mapping = {"₹": "Low", "₹₹": "Medium", "₹₹₹": "High"}
                budget = budget  # Convert display to actual text

                # Construct the prompt message for GPT-4 based on user inputs
                prompt = f"""
                I am a {age}-year-old {gender} with a height of {total_height_inches} inches and a weight of {weight} kg. 
                I follow a {diet_type} diet. I would like a weekly diet plan that includes {weekly_variety} unique meals. 
                My budget is {budget}. Additionally, I dislike or am allergic to the following foods: {dislikes}.
                Please generate a detailed and personalized nutrition diet plan for me.
                """
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(contents=prompt)
            # Display the generated diet plan on the Streamlit app
            st.success("Here is your personalized diet plan:")
            st.write(response.text)
