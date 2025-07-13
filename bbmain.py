import gradio as gr
from logic.bbbsignup import start_signup_async, submit_code_async ,sec_submit_code_async

def run_app():
    with gr.Blocks() as demo:
        output = gr.Textbox(label="Output", interactive=False, lines=5)
        code_input_1 = gr.Textbox(label="Enter verification code", visible=False)
        code_input_2 = gr.Textbox(label="Enter 2FA code (Second verification)", visible=False)

        start_btn = gr.Button("Start Signup")
        verify_btn = gr.Button("Confirm Email Verification")
        verify2_btn = gr.Button("Confirm 2FA Code")

        start_btn.click(
            fn=start_signup_async,
            outputs=[output, code_input_1]
        )

        verify_btn.click(
            fn=submit_code_async,
            inputs=code_input_1,
            outputs=[output, code_input_1, code_input_2]
        )

        verify2_btn.click(
            fn=sec_submit_code_async,
            inputs=code_input_2,
            outputs=[output]
        )

    demo.launch()


gradio_app = run_app()


# Mount to FastAPI
app = FastAPI()
app = mount_gradio_app(app, gradio_app, path="/")
