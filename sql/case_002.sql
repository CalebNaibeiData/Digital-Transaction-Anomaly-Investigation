-- Exhibit 1: chronological account access and transfers
SELECT t.transaction_id,t.timestamp_utc,t.sender_id,t.recipient_id,t.amount_kes,t.session_device_id
FROM transactions t WHERE t.sender_id='A100' ORDER BY t.timestamp_utc;

-- Exhibit 2: account and device correlation
SELECT a.account_id,a.device_id,a.event_type,a.result,a.timestamp_utc
FROM auth_events a WHERE a.device_id='D9' ORDER BY a.timestamp_utc;

-- Exhibit 3: inbound and outbound value at intermediary accounts
SELECT sender_id AS account_id, SUM(amount_kes) AS outgoing_kes, COUNT(*) AS transfer_count
FROM transactions WHERE status='SUCCESS' GROUP BY sender_id ORDER BY outgoing_kes DESC;

-- Exhibit 4: recipients and transfer concentration
SELECT recipient_id,COUNT(*) AS inbound_count,SUM(amount_kes) AS inbound_kes
FROM transactions WHERE status='SUCCESS' GROUP BY recipient_id ORDER BY inbound_kes DESC;
