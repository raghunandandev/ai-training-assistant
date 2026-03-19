import streamlit as st
import io
from pptx import Presentation
from processors import DocumentProcessor
from ai_engine import AIEngine
from tracker import ComplianceTracker

# --- HELPER FUNCTION FOR PPTX GENERATION (Bonus 2) ---
def create_ppt(training_data):
    prs = Presentation()
    
    # Title Slide
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = training_data.get("title", "Training Module")
    subtitle.text = "Generated AI Training Presentation"

    # Summary Slide
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    shapes = slide.shapes
    title_shape = shapes.title
    body_shape = shapes.placeholders[1]
    title_shape.text = "Executive Summary"
    tf = body_shape.text_frame
    tf.text = training_data.get("summary", "")

    # Steps Slides
    for i, step in enumerate(training_data.get("steps", [])):
        slide = prs.slides.add_slide(bullet_slide_layout)
        shapes = slide.shapes
        title_shape = shapes.title
        body_shape = shapes.placeholders[1]
        title_shape.text = f"Step {i+1}"
        tf = body_shape.text_frame
        tf.text = step

    # Save to memory stream
    ppt_stream = io.BytesIO()
    prs.save(ppt_stream)
    ppt_stream.seek(0)
    return ppt_stream

# --- MAIN APP LOGIC ---
def main():
    st.set_page_config(page_title="AI Training System", layout="wide")
    st.title("📄 SOP to AI Training System")
    st.write("Upload a standard operating procedure to instantly generate a training module, slide deck, and compliance quiz.")

    # Initialize objects
    try:
        ai = AIEngine()
    except Exception as e:
        st.error(f"Setup Error: {str(e)}")
        return

    tracker = ComplianceTracker()

    # Session state to hold data so it doesn't disappear on button clicks
    if "training_data" not in st.session_state:
        st.session_state.training_data = None
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    # 1. File Upload
    uploaded_file = st.file_uploader("Upload SOP (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        if st.button("Generate Training Materials", type="primary"):
            with st.spinner("Extracting text and generating AI curriculum..."):
                doc = DocumentProcessor(uploaded_file)
                extracted_text = doc.extract_text()
                
                if extracted_text.startswith("Error"):
                    st.error(extracted_text)
                else:
                    data = ai.generate_training_module(extracted_text)
                    if "error" in data:
                        st.error(data["error"])
                    else:
                        st.session_state.training_data = data
                        st.session_state.quiz_submitted = False
                        st.rerun()

    # 2. Display the UI if data exists
    if st.session_state.training_data:
        data = st.session_state.training_data
        st.divider()
        st.header(data.get("title", "Training Module"))
        
        # Download PPTX Button
        ppt_file = create_ppt(data)
        st.download_button(
            label="📥 Download Presentation (.pptx)",
            data=ppt_file,
            file_name="training_presentation.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

        # Tabs for Content
        tab1, tab2, tab3 = st.tabs(["📑 Summary", "⚙️ Step-by-Step", "🎓 Evaluation Quiz"])

        with tab1:
            st.subheader("Module Overview")
            st.info(data.get("summary", "No summary available."))

        with tab2:
            st.subheader("Process Steps")
            for i, step in enumerate(data.get("steps", [])):
                st.markdown(f"**{i+1}.** {step}")

        with tab3:
            st.subheader("Knowledge Check")
            # Form for the quiz
            with st.form("quiz_form"):
                # Removed required=True
                user_name = st.text_input("Employee Name:") 
                
                user_answers = {}
                for i, q in enumerate(data.get("quiz", [])):
                    st.markdown(f"**Q{i+1}: {q['question']}**")
                    user_answers[i] = st.radio("Select answer:", q['options'], key=f"q_{i}")
                    st.write("")
                
                submitted = st.form_submit_button("Submit Answers")
                
                if submitted:
                    # Manual check to ensure they entered a name
                    if not user_name.strip():
                        st.warning("⚠️ Please enter your Employee Name before submitting.")
                    else:
                        correct_count = 0
                        for i, q in enumerate(data.get("quiz", [])):
                            if user_answers[i] == q['answer']:
                                correct_count += 1
                        
                        total = len(data.get("quiz", []))
                        score_str = f"{correct_count}/{total}"
                        
                        # Use tracker object to save data (Automation Bonus)
                        tracker.log_score(user_name, data.get("title", "Unknown SOP"), score_str)
                        
                        st.success(f"Quiz submitted! You scored {score_str}.")
                        st.info("Your score has been automatically logged to the compliance database.")
            
            # # Form for the quiz
            # with st.form("quiz_form"):
            #     user_name = st.text_input("Employee Name:", required=True)
                
            #     user_answers = {}
            #     for i, q in enumerate(data.get("quiz", [])):
            #         st.markdown(f"**Q{i+1}: {q['question']}**")
            #         user_answers[i] = st.radio("Select answer:", q['options'], key=f"q_{i}")
            #         st.write("")
                
            #     submitted = st.form_submit_button("Submit Answers")
                
            #     if submitted:
            #         correct_count = 0
            #         for i, q in enumerate(data.get("quiz", [])):
            #             if user_answers[i] == q['answer']:
            #                 correct_count += 1
                    
            #         total = len(data.get("quiz", []))
            #         score_str = f"{correct_count}/{total}"
                    
            #         # Use tracker object to save data (Automation Bonus)
            #         tracker.log_score(user_name, data.get("title", "Unknown SOP"), score_str)
                    
            #         st.success(f"Quiz submitted! You scored {score_str}.")
            #         st.info("Your score has been automatically logged to the compliance database.")

if __name__ == "__main__":
    main()