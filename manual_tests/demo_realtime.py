import asyncio

from src.audio.stream import AudioStream
from src.realtime.relatime import OpenAIRealtimeAPIWrapper


async def main() -> None:
    """Demo for OpenAI Realtime API client."""
    stream = AudioStream()
    client = OpenAIRealtimeAPIWrapper(stream)

    # Start background tasks
    asyncio.create_task(stream.run())

    try:
        await client.connect(audio_enabled=True)
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping demo...")
        # await client.configure_session(
        #     voice="en-US", temperature=0.7, system_message="You are a helpful assistant."
        # )

        # audio_stream = client.listen_audio_responses()
        # await client.start_audio_stream(audio_stream)

        # async for event in client.listen_events():
        #     print(f"Received event: {event}")

        # await client.send_event({"type": "test_event", "data": "Hello, World!"})

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
