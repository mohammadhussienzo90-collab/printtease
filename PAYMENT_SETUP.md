# Payment Gateway Setup Guide

## Option 1: Stripe (Recommended - Easiest Setup)

### Step 1: Create Stripe Account
1. Go to https://stripe.com and sign up
2. Verify your email address
3. Complete Stripe onboarding (they'll ask for basic business info)

### Step 2: Get API Keys
1. Go to Dashboard → Developers → API Keys
2. Copy your **Publishable Key** (starts with `pk_test_...`)
3. Copy your **Secret Key** (starts with `sk_test_...`)

### Step 3: Add to Railway Environment Variables
```
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Update Code
Install stripe:
```bash
pip install stripe
```

Create `payments/views.py`:
```python
import stripe
from django.conf import settings
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(request):
    amount = request.POST.get('amount', 5000)  # Amount in cents
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency='usd',
            automatic_payment_methods={'enabled': True},
        )
        return JsonResponse({'clientSecret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
```

### Step 5: Frontend Integration
Add Stripe.js to your checkout template:
```html
<script src="https://js.stripe.com/v3/"></script>
<script>
    const stripe = Stripe('{{ STRIPE_PUBLISHABLE_KEY }}');
    // Handle payment form submission
</script>
```

---

## Option 2: PayPal (Good Alternative)

### Step 1: Create PayPal Developer Account
1. Go to https://developer.paypal.com
2. Sign in with your PayPal account

### Step 2: Get Credentials
1. Go to Dashboard → My Apps & Credentials
2. Create a new app
3. Copy **Client ID** and **Secret**

### Step 3: Add to Railway
```
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_SECRET=your_secret
PAYPAL_MODE=sandbox  # Change to 'live' for production
```

---

## Option 3: Razorpay (Popular in Middle East/India)

### Step 1: Create Razorpay Account
1. Go to https://razorpay.com
2. Sign up and complete KYC

### Step 2: Get Keys
1. Go to Settings → API Keys
2. Copy Key ID and Key Secret

### Step 3: Add to Railway
```
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
```

---

## Quick Comparison

| Feature | Stripe | PayPal | Razorpay |
|---------|--------|--------|----------|
| Ease of Setup | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Transaction Fees | 2.9% + $0.30 | 2.9% + $0.30 | 2% |
| Global Coverage | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Egypt Support | ✅ | ✅ | ❌ |

---

## Railway Deployment Steps

1. **Push to GitHub** (instructions below)
2. **Create Railway Project**
   - Go to https://railway.app
   - Connect your GitHub repo
3. **Add Environment Variables**
   - Add all payment gateway keys
   - Set `DEBUG=False`
4. **Deploy**
   - Railway will auto-deploy on push
5. **Custom Domain**
   - Go to project → Settings → Domains
   - Add your domain
   - Update DNS records

---

## GitHub Push Instructions

Since GitHub CLI has issues, here's how to push manually:

1. **Create GitHub Repository:**
   - Go to https://github.com/new
   - Name: `pink-toy-store`
   - Make it public or private
   - Don't add README (we have existing files)

2. **Push from your terminal:**
```bash
cd C:\Users\Egypt Store\source\repos\storefront\storefront

git add .
git commit -m "Initial commit: Pink Toy Store with admin and payment ready"

git remote add origin https://github.com/YOUR_USERNAME/pink-toy-store.git

git branch -M main
git push -u origin main
```

3. **Update Railway:**
   - Connect the new repo to Railway
   - Deploy

---

## Current Project Structure
```
pink-toy-store/
├── accounts/          # User authentication
├── carts/            # Shopping cart
├── orders/            # Order management
├── products/          # Product catalog (with admin)
├── templates/         # HTML templates (pink theme)
├── storefront/       # Django settings
├── requirements.txt   # Dependencies
├── Procfile           # Railway web process
├── runtime.txt        # Python version
└── .gitignore        # Git ignore rules
```