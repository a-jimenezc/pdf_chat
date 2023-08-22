import asyncio
import websockets
import json

async def main():
    async with websockets.connect('ws://127.0.0.1:5000/api/v2/generate') as ws:
        # Send open_inference_session request
        await ws.send(json.dumps({
            "type": "open_inference_session",
            "max_length": 1024
        }))
        
        # Receive open_inference_session response
        response = await ws.recv()
        response_data = json.loads(response)
        if response_data.get("ok"):
            print("Inference session opened successfully.")
        else:
            print("Failed to open inference session.")
            return
        
        # Send generate requests
        while True:
            generate_request = {
                "type": "generate",
                "inputs": "sabes hablar español? \"",
                "max_new_tokens": 30
            }
            await ws.send(json.dumps(generate_request))
            
            # Receive generate response
            response = await ws.recv()
            response_data = json.loads(response)
            if response_data.get("ok"):
                outputs = response_data.get("outputs")
                stop = response_data.get("stop")
                if outputs is not None:
                    print("Generated:", outputs)
                if stop:
                    print("Generation complete.")
                    break
            else:
                print("Failed to generate.")
                break

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())



