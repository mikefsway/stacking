# Deployment Guide - Streamlit Cloud

## Quick Deployment Steps

### 1. Prepare Your GitHub Repository

1. Create a new repository on GitHub (e.g., `energy-revenue-stacking`)
2. Initialize git in your streamlit-app folder:

```bash
cd streamlit-app
git init
git add .
git commit -m "Initial commit: Revenue Stacking Tool"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/energy-revenue-stacking.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Configure deployment:
   - **Repository**: `YOUR_USERNAME/energy-revenue-stacking`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **Python version**: 3.9+ (recommended)

5. Click "Deploy!"

Your app will be live at: `https://YOUR_USERNAME-energy-revenue-stacking.streamlit.app`

## Repository Structure

Your GitHub repo should have this structure:

```
energy-revenue-stacking/
├── app.py                      # ← Main file path
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml
├── data/
│   └── stacking_data.json
├── modules/
│   ├── __init__.py
│   └── ui_components.py
└── utils/
    ├── __init__.py
    ├── data_loader.py
    └── descriptions.py
```

## Pre-Deployment Checklist

- [ ] All files committed to git
- [ ] `requirements.txt` includes all dependencies
- [ ] `data/stacking_data.json` is present
- [ ] `.gitignore` excludes unnecessary files
- [ ] README.md is complete and helpful
- [ ] No hardcoded secrets or API keys

## Post-Deployment Testing

After deployment, test:

1. ✅ App loads without errors
2. ✅ Services can be selected from dropdown
3. ✅ Compatibility results display correctly
4. ✅ Service details show with descriptions
5. ✅ Matrix view renders properly
6. ✅ Tooltips work (hover over ℹ️ icons)
7. ✅ Responsive design works on mobile

## Updating Your Deployed App

To update the live app:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push

# Streamlit Cloud will automatically redeploy!
```

## Custom Domain (Optional)

To use a custom domain:

1. Go to your app settings on Streamlit Cloud
2. Click "General" → "Custom subdomain"
3. Enter your preferred subdomain
4. Follow DNS configuration instructions

## Environment Variables (If Needed)

If you need to add secrets or environment variables:

1. Go to app settings on Streamlit Cloud
2. Click "Secrets"
3. Add your secrets in TOML format:

```toml
[api_keys]
my_key = "secret_value"
```

Access in your app:
```python
import streamlit as st
my_key = st.secrets["api_keys"]["my_key"]
```

## Troubleshooting

### App Won't Deploy

**Issue**: "ModuleNotFoundError"
- **Solution**: Add missing module to `requirements.txt`

**Issue**: "File not found: data/stacking_data.json"
- **Solution**: Ensure data file is committed to git

**Issue**: "Python version incompatible"
- **Solution**: Specify Python version in Streamlit Cloud settings (3.9+)

### App Runs Slowly

- Use `@st.cache_resource` for data loading (already implemented)
- Minimize data processing in main loop
- Consider reducing dataset size if too large

### App Shows Errors

1. Check Streamlit Cloud logs:
   - Go to your app dashboard
   - Click "Manage app" → "Logs"
   - Look for Python exceptions

2. Test locally first:
   ```bash
   streamlit run app.py
   ```

## Performance Optimization

### Caching

Already implemented:
```python
@st.cache_resource
def load_data():
    loader = StackingDataLoader()
    loader.load_data()
    return loader
```

### Further Optimizations

1. **Lazy loading**: Load data only when needed
2. **Pagination**: For large compatibility matrices
3. **Compression**: Compress large JSON data files

## Monitoring

### Usage Analytics

Streamlit Cloud provides basic analytics:
- Unique visitors
- Page views
- Session duration

Access via app dashboard → Analytics

### Error Tracking

Monitor errors in Streamlit Cloud logs:
- App dashboard → Manage app → Logs
- Set up alerts for critical errors

## Security

### Best Practices

- ✅ No sensitive data in repository
- ✅ Use secrets management for API keys
- ✅ Enable XSRF protection (in config.toml)
- ✅ Validate user inputs
- ✅ Keep dependencies updated

### Data Privacy

The app processes data client-side (in browser):
- No user data sent to external servers
- No tracking or analytics beyond Streamlit's built-in
- All calculations happen in the Streamlit session

## Backup Strategy

### Regular Backups

1. **Code**: Already backed up in GitHub
2. **Data**: `stacking_data.json` in repository
3. **Configuration**: `.streamlit/config.toml` in repository

### Version Control

Use git tags for releases:
```bash
git tag -a v1.0 -m "Initial release"
git push origin v1.0
```

## Scaling Considerations

### Current Setup
- Free Streamlit Cloud tier: Suitable for moderate traffic
- Single-instance deployment

### If Traffic Increases
- Upgrade to Streamlit Cloud Team or Enterprise
- Consider self-hosting on AWS/GCP/Azure
- Implement caching strategies
- Use CDN for static assets

## Support Resources

- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: For bug reports

## Maintenance Schedule

### Regular Tasks

- **Weekly**: Check app performance and logs
- **Monthly**: Update dependencies (`pip list --outdated`)
- **Quarterly**: Review and update data (`stacking_data.json`)
- **Annually**: Review technical requirements for service changes

### Dependency Updates

```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade streamlit

# Update requirements.txt
pip freeze > requirements.txt

# Test locally, then commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push
```

## Cost Considerations

### Streamlit Cloud Free Tier
- ✅ 1 private app
- ✅ Unlimited public apps
- ✅ Community support
- ✅ Adequate for this project

### Paid Tiers (If Needed)
- **Starter**: $20/month - Multiple private apps
- **Team**: $250/month - Collaboration features
- **Enterprise**: Custom pricing - Advanced features

For this tool, **free tier should be sufficient**.

## Success Metrics

Track these metrics:
- Number of unique users
- Average session duration
- Most compared service pairs
- Common compatibility queries

Use this data to:
- Improve UI/UX
- Add popular features
- Update documentation
- Prioritize service updates

---

**Ready to Deploy?** Follow the steps above and your app will be live in minutes! 🚀
