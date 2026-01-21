"""
Manual Token Entry - Simple version

Just paste your token here and it will be saved.
"""

import json
from datetime import datetime

print("\n" + "="*70)
print("MANUAL TOKEN ENTRY")
print("="*70)
print("\nHow to get your token:")
print("1. Open https://apps.paybooks.in/ in Chrome")
print("2. Login with your credentials")
print("3. Press F12 to open Developer Tools")
print("4. Click 'Network' tab")
print("5. Click on any payslip")
print("6. Find 'PayslipDownload' in the network requests")
print("7. Click on it -> 'Payload' tab")
print("8. Scroll down to 'Request Payload'")
print("9. Copy the entire 'requestData' value (long base64 string)")
print("10. OR if you see 'LoginToken' directly, copy that")
print("="*70)

token_input = input("\nPaste your token here and press Enter: ").strip()

if not token_input:
    print("❌ No token entered")
    exit(1)

# Check if it's a base64 requestData or direct token
if len(token_input) > 100:
    # Might be the full request data, try to decode
    try:
        import base64
        from urllib.parse import unquote
        
        # Try to unquote if URL encoded
        if '%' in token_input:
            token_input = unquote(token_input)
        
        # Try to decode as base64
        decoded = base64.b64decode(token_input).decode('utf-8')
        payload = json.loads(decoded)
        token = payload.get('LoginToken')
        
        if token:
            print(f"\n✅ Extracted LoginToken from request data")
        else:
            print("❌ Could not find LoginToken in the data")
            exit(1)
    except:
        # Maybe it's already the token
        token = token_input
else:
    token = token_input

# Save token
token_data = {
    "token": token,
    "timestamp": datetime.now().isoformat()
}

with open('.paybooks_token', 'w') as f:
    json.dump(token_data, f, indent=2)

print(f"\n💾 Token saved to .paybooks_token")
print(f"   Token preview: {token[:30]}...{token[-20:]}")
print(f"\n✅ SUCCESS! You can now run: python sync_payslips.py\n")
