async def transcribe_progress(self, event):
  await self.send(text_data=json.dumps({
      'status': event['status'],
      'progress': event['progress'],
      'message': event['message'],
      }))