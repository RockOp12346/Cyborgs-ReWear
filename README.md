# ReWear – Community Clothing Exchange 👚♻️

## Problem Statement:-
## ReWear – Community Clothing Exchange
Develop ReWear, a web-based platform that enables users to exchange unused clothing 
through direct swaps or a point-based redemption system. The goal is to promote sustainable 
fashion and reduce textile waste by encouraging users to reuse wearable garments instead of 
discarding them.

**ReWear** is a web-based platform that promotes sustainable fashion by allowing users to exchange unused clothing through either **direct swaps** or a **point-based redemption system**. The project aims to reduce textile waste and encourage a culture of reuse and conscious consumption.

---

## 🌱 Why ReWear?

Every year, millions of tons of wearable clothes are discarded, contributing significantly to environmental pollution. ReWear tackles this issue by providing a digital space where people can give their unused garments a second life — all while saving money, earning points, and promoting a greener planet.

---

## 💡 Key Features

### 👤 User Authentication
- Secure login and registration using email and password.
- Session-based authentication for user data safety.

### 🏠 Landing Page
- Platform overview with featured items carousel.
- Clear calls to action: **Start Swapping**, **Browse Items**, and **List an Item**.

### 📊 User Dashboard
- Profile info with points balance.
- List of uploaded clothing items.
- Record of ongoing and completed swaps.

### 👗 Item Management
- **Add New Item**: Upload images, add title, description, size, category, tags, and condition.
- **Item Detail Page**: View full details, availability status, and action buttons (Swap Request / Redeem via Points).
- Browse and search functionality by category or tag.

### 🔄 Swap and Points System
- Two exchange methods:
  - **Direct Swap**: Users can initiate a swap for listed items.
  - **Point System**: Earn points by giving clothes; redeem points to receive new items.

### 🛠️ Admin Panel
- Approve or reject submitted items.
- Remove inappropriate listings or spam content.
- Light dashboard for moderation and report generation.

---

## 🧱 Tech Stack

- **Frontend**: JavaScript, Tailwind CSS
- **Backend**: Django
- **Database**: SQLite
- **Authentication**: JWT & Bcrypt
- **Storage**: Cloudinary for image uploads

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- MongoDB instance (local or Atlas)

### Installation
```bash
git clone https://github.com/yourusername/ReWear.git
cd ReWear
npm install
