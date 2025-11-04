from datetime import timedelta
from typing import Dict, Any, List, Tuple, Optional
from firebase_admin import messaging

class FcmNotificationSender:
    def send_to_tokens(self, tokens: List[str], title: str, body: str,
                       data: Dict[str, Any], priority: str, ttl: int) -> List[Tuple[str,bool,Optional[str]]]:
        if not tokens:
            return []
        msg = messaging.MulticastMessage(
            tokens=tokens,
            notification=messaging.Notification(title=title, body=body),
            data={k: str(v) for k,v in (data or {}).items()},
            android=messaging.AndroidConfig(priority=("high" if priority=="HIGH" else "normal"),
                                            ttl=timedelta(seconds=ttl)),
            apns=messaging.APNSConfig(headers={"apns-priority": "10"}),
            webpush=messaging.WebpushConfig(headers={"Urgency": "high" if priority=="HIGH" else "normal"}),
        )
        res = messaging.send_each_for_multicast(msg)
        out = []
        for i, r in enumerate(res.responses):
            if r.success:
                out.append((tokens[i], True, None))
            else:
                code = getattr(r.exception, "code", None)
                out.append((tokens[i], False, code))
        return out
