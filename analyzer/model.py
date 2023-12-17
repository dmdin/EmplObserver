from dataclasses import dataclass, asdict
from datetime import date

@dataclass()
class UserStatisticItem:
    sent_messages_count: int
    received_messages_count: int 
    recipient_counts: int
    bcc_count: int 
    cc_count: int 
    days_between_received_and_read: int
    replied_messages_count: int 
    sent_characters_count: int 
    messages_outside_working_hours: int 
    received_to_sent_ratio: float
    bytesReceivedToSentRatio: float
    messages_with_question_and_no_reply: int
    read_messages_later_than: int
    count_events: int
    endInterval: date

    def dict(self):
        return {k: v for k, v in asdict(self).items()}