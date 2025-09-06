# Railway Deployment Guide 🚂

This guide will help you deploy the Galxe Alert Bot on Railway, a cloud platform that can run your Python application 24/7.

## Prerequisites 📋

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Telegram Bot Token**: Get from [@BotFather](https://t.me/BotFather)
4. **Telegram Channel**: Create a channel and get its ID

## Step 1: Prepare Your Repository 🛠️

Make sure your repository contains all the necessary files:
- `main.py` - Main bot script
- `config.py` - Configuration file
- `requirements.txt` - Python dependencies
- `Procfile` - Railway process file
- `railway.json` - Railway configuration
- All other Python files (database.py, scraper.py, telegram_bot.py, etc.)

## Step 2: Deploy to Railway 🚀

### Method 1: Deploy from GitHub (Recommended)

1. **Login to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository containing the Galxe Alert Bot

3. **Configure Environment Variables**
   - Go to your project dashboard
   - Click on "Variables" tab
   - Add the following environment variables:

   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHANNEL_ID=@your_channel_username_or_id
   SCRAPING_INTERVAL_MINUTES=30
   LOG_LEVEL=INFO
   ```

4. **Deploy**
   - Railway will automatically detect the Python project
   - It will install dependencies from `requirements.txt`
   - The bot will start running using the `Procfile`

### Method 2: Deploy with Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   railway init
   ```

4. **Set Environment Variables**
   ```bash
   railway variables set TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   railway variables set TELEGRAM_CHANNEL_ID=@your_channel_username_or_id
   railway variables set SCRAPING_INTERVAL_MINUTES=30
   railway variables set LOG_LEVEL=INFO
   ```

5. **Deploy**
   ```bash
   railway up
   ```

## Step 3: Configure Your Telegram Bot 🤖

1. **Create Bot**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Save the bot token

2. **Create Channel**
   - Create a new Telegram channel
   - Add your bot as an administrator
   - Get the channel ID:
     - For public channels: Use `@channel_username`
     - For private channels: Forward a message from your channel to [@userinfobot](https://t.me/userinfobot) to get the numeric ID

3. **Set Environment Variables**
   - Add your bot token and channel ID to Railway environment variables

## Step 4: Monitor Your Deployment 📊

1. **Check Logs**
   - Go to your Railway project dashboard
   - Click on "Deployments" tab
   - Click on the latest deployment
   - View logs to see if the bot is running correctly

2. **Monitor Status**
   - The bot should start automatically
   - Check logs for startup messages
   - Look for "Bot started successfully and ready to monitor!" message

## Step 5: Test Your Bot ✅

1. **Check Telegram**
   - The bot should send a test message to your channel
   - Look for quest notifications every 30 minutes (or your configured interval)

2. **Monitor Logs**
   - Check Railway logs for any errors
   - Look for successful quest scraping messages

## Environment Variables Reference 🔧

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token from @BotFather | - | ✅ |
| `TELEGRAM_CHANNEL_ID` | Your Telegram channel ID or username | - | ✅ |
| `SCRAPING_INTERVAL_MINUTES` | How often to check for new quests (minutes) | 30 | ❌ |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO | ❌ |
| `DATABASE_PATH` | Path to SQLite database file | quests.db | ❌ |
| `LOG_FILE` | Path to log file | bot.log | ❌ |

## Troubleshooting 🔧

### Common Issues

1. **Bot Not Starting**
   - Check environment variables are set correctly
   - Verify Telegram bot token is valid
   - Check Railway logs for error messages

2. **Selenium Issues**
   - Railway automatically installs Chrome and ChromeDriver
   - If issues persist, check logs for Selenium errors

3. **No Quest Notifications**
   - Verify channel ID is correct
   - Check if bot is added to channel as admin
   - Monitor logs for scraping errors

4. **Memory Issues**
   - Railway provides limited memory
   - The bot is optimized for cloud deployment
   - Consider upgrading Railway plan if needed

### Log Analysis

Look for these key messages in Railway logs:
- ✅ `Bot started successfully and ready to monitor!`
- ✅ `Found X new quests for ProjectName`
- ❌ `Error checking project` - indicates scraping issues
- ❌ `Failed to connect to Telegram` - indicates bot token issues

## Railway Plan Considerations 💰

- **Free Plan**: Limited resources, may have restrictions
- **Pro Plan**: Better performance, more resources
- **Team Plan**: For multiple deployments

## Updating Your Bot 🔄

1. **Push Changes to GitHub**
   ```bash
   git add .
   git commit -m "Update bot"
   git push origin main
   ```

2. **Railway Auto-Deploy**
   - Railway will automatically detect changes
   - It will redeploy your application
   - Check logs to ensure successful deployment

## Security Notes 🔒

- Never commit your `.env` file to GitHub
- Use Railway environment variables for sensitive data
- Keep your Telegram bot token secure
- Regularly update dependencies

## Support 📞

If you encounter issues:
1. Check Railway logs first
2. Verify all environment variables are set
3. Test your Telegram bot manually
4. Check the troubleshooting section above

---

**Your Galxe Alert Bot is now running 24/7 on Railway! 🎉**

The bot will automatically:
- Monitor all configured Galxe projects
- Check for new quests every 30 minutes (configurable)
- Send notifications to your Telegram channel
- Handle errors gracefully and restart if needed
