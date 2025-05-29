import streamlit as st

st.title("🎉 Mad Libs Generator")

st.write("Fill in the blanks and click 'Create Story' to see your Mad Lib!")

# Input fields
noun = st.text_input("Enter a noun:")
verb = st.text_input("Enter a verb:")
adjective = st.text_input("Enter an adjective:")
place = st.text_input("Enter a place:")
person = st.text_input("Enter a person's name:")

# Button to generate the story
if st.button("Create Story"):
   if noun and verb and adjective and place and person:
       story = f"""
       One day, {person} went to the {place}.
       There, they saw a very {adjective} {noun}.
       Without thinking, they decided to {verb} it.
       It was the beginning of an unforgettable adventure!
                                                    """
       st.subheader("📝 Your Story:")
       st.write(story)
   else:
        st.warning("Please fill in all the blanks to create your story.")
            