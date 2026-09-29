# Incremental Loading

Python ETL pipeline demonstrating incremental data loading from an API into PostgreSQL.

# Incremental API to PostgreSQL ETL

## Overview

This project demonstrates an incremental ETL pipeline that extracts user data from an API and loads it into PostgreSQL.

## Pipeline

API
↓
Extract
↓
Transform & Validate
↓
Incremental Load
↓
PostgreSQL

## Features

- API data extraction using Python
- Data validation and rejection handling
- PostgreSQL loading
- Incremental loading
- Insert new records
- Update changed records
- Skip unchanged records
- Logging
- Environment variables using `.env`

## Incremental Loading Logic

The pipeline checks the existing data and determines whether each record should be:

- Inserted
- Updated
- Skipped

Example:

Inserted: 0  
Updated: 0  
Skipped: 10

This prevents unnecessary updates when the source data has not changed.
