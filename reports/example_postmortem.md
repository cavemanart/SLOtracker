# Postmortem: API Latency Spike - July 2025

## Summary
High latency on User Login service during peak hours.

## Root Cause
Database index regression caused p95 latency to exceed 300ms.

## Impact
Login delays for ~5% of users over 2 hours.

## Actions
- Re-indexed affected DB table
- Added latency regression alert
- Improved CI test for latency thresholds

## Status
All actions complete. Postmortem closed.
