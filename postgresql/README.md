# 🧠 Maths Challenge – PostgreSQL Setup Guide

This folder contains the SQL schema and instructions to manage the database for the **Maths Challenge** backend.

---

## 🗃️ What’s Inside

- `schema.sql`: Creates the `generated_problems` table to store dynamic word problems, user attempts, and correctness.

---

## 🧪 How to Run the Schema

Make sure:
- PostgreSQL is installed and running
- You’ve created a database named `maths_challenge`

### ✅ Step-by-Step:

1. **Open Terminal**

2. **Navigate to project root:**
   ```bash
   cd autodidact

for runnig the schema.sql file

psql -d maths_challenge -f autodidact/postgresql/schema.sql
