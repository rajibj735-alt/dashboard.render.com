import telebot
import os
from PIL import Image, ImageDraw, ImageFont

# আপনার দেওয়া টোকেনটি এখানে বসানো হয়েছে
BOT_TOKEN = '8972532362:AAGP0CKJOKxrBbsmHz2xRhaet9HWtU050qw'
bot = telebot.TeleBot(BOT_TOKEN)

# ১. কেউ /start দিলে তাকে স্বাগতম জানাবে
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম! আমাকে একটি ছবি পাঠান, আমি সেটিতে টেক্সট যোগ করে দেব।")

# ২. ইউজার ছবি পাঠালে সেটি রিসিভ এবং এডিট করবে
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "ছবিটি পাওয়া গেছে। প্রসেসিং হচ্ছে, একটু অপেক্ষা করুন...")
        
        # ছবি ডাউনলোড করার প্রসেস
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        input_path = "user_photo.jpg"
        output_path = "edited_photo.jpg"
        
        with open(input_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        # Pillow দিয়ে ছবি এডিট করা[span_2](start_span)[span_2](end_span)
        img = Image.open(input_path)
        draw = ImageDraw.Draw(img)
        
        # ছবির ওপরে একটি প্রমোশনাল টেক্সট লেখা
        text = "Online Earning From Home"
        draw.text((30, 30), text, fill=(255, 255, 0)) # হলুদ রঙের লেখা
        
        # এডিটেড ছবি সেভ করা
        img.save(output_path)
        
        # ইউজারের কাছে ছবি ফেরত পাঠানো
        with open(output_path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="আপনার এডিটেড ছবি রেডি!")
            
        # কাজ শেষে সাময়িক ফাইল ডিলিট করা
        os.remove(input_path)
        os.remove(output_path)

    except Exception as e:
        bot.reply_to(message, f"একটি সমস্যা হয়েছে: {e}")

# বট চালু রাখা
if __name__ == "__main__":
    print("বটটি চালু হচ্ছে...")
    bot.infinity_polling()