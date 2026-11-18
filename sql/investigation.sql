-- Read-only investigation queries on synthetic records
SELECT recipient_id, COUNT(*) AS transfers, COUNT(DISTINCT sender_id) AS unique_senders,
       SUM(amount_kes) AS total_kes
FROM transactions WHERE status = 'SUCCESS'
GROUP BY recipient_id HAVING COUNT(DISTINCT sender_id) >= 8
ORDER BY unique_senders DESC, transfers DESC;

SELECT sender_id, recipient_id, COUNT(*) AS transfers, SUM(amount_kes) AS total_kes
FROM transactions WHERE status = 'SUCCESS'
GROUP BY sender_id, recipient_id HAVING COUNT(*) >= 8
ORDER BY transfers DESC;

SELECT transaction_id, timestamp_utc, sender_id, recipient_id, amount_kes
FROM transactions WHERE sender_id = 'U007' AND recipient_id = 'U099'
ORDER BY timestamp_utc;
