# Image uploader
bucket_name= voice-rag
object_name = f'https://{bucket_name}.s3.us-west-1.amazonaws.com/output_microphone_audio1.wav'
s3_client.upload_fileobj(buffer, 'gpt4o-funtest', object_name)
st.session_state['s3_image_url'] = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"

