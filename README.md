# Inuno.ai Project

**Inuno.ai** is a Django-powered platform designed to aggregate and organize news dynamically using AI and RSS feeds. It features a responsive frontend built with Django templates, HTML, and CSS, and a robust backend for managing news, user accounts, and more.

---

## **Features**

### General
- **News Aggregation**: Fetch news from multiple sources using AI and RSS feeds, categorizing them automatically.  
- **Trending and Editor's Picks**: Highlight trending topics and articles flagged as editor's picks.  
- **Dynamic Categories**: Supports categories and subcategories for better organization.  

### Frontend
- Built with Django templates, HTML, and CSS.  
- Responsive and user-friendly design.  

### Backend
- **Custom Authentication**: Token-based authentication with Django REST Framework.  
- **Dynamic Querying**: Efficient APIs for retrieving and filtering data.  
- **Custom Short Unique IDs**: Articles are assigned unique IDs like `128UYh78`.  

---

## **Installation**

1. Clone the repository:  
   ```bash
   git clone https://github.com/Omofon/inuno.ai.git
   cd inuno.ai
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser for admin access:  
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:  
   ```bash
   python manage.py runserver
   ```

6. Access the site at `http://127.0.0.1:8000`.

---

## **API Endpoints**

### Authentication (`accounts` app)
| **Path**               | **View**                     | **Description**                                 | **Name**                 |
|-------------------------|------------------------------|-------------------------------------------------|--------------------------|
| `login/`               | `login_view`                | Displays the login page and processes user login. | `login`                  |
| `signup/`              | `register_view`             | Handles user registration.                      | `signup`                 |
| `logout/`              | `logout_view`               | Logs the user out.                              | `logout`                 |
| `profile/`             | `UserProfileView`           | Displays and manages the user's profile.        | `user_profile`           |
| `delete/`              | `DeleteUserView`            | Deletes the user's account.                     | `delete_user`            |
| `password-reset/`      | `auth_views.PasswordResetView`| Initiates password reset by sending a reset email. | `password_reset`         |
| `password-reset/done/` | `auth_views.PasswordResetDoneView`| Confirmation page after the password reset email is sent. | `password_reset_done` |
| `reset/<uidb64>/<token>/` | `auth_views.PasswordResetConfirmView` | Handles token-based password reset confirmation. | `password_reset_confirm` |
| `reset/done/`          | `auth_views.PasswordResetCompleteView` | Password reset completion page.                | `password_reset_complete`|

### News (`news` app)
| **Path**                     | **View**                         | **Description**                                        | **Name**                   |
|-------------------------------|-----------------------------------|--------------------------------------------------------|----------------------------|
| `/`                          | `HomePageView`                   | Displays the homepage with a summary of news.         | `home`                     |
| `articles/`                  | `ArticleListView`                | Lists all articles.                                   | `article_list`             |
| `articles/<slug:slug>/`      | `ArticleDetailView`              | Displays a specific article by slug.                 | `article_detail`           |
| `category/<slug:slug>/`      | `ArticlesByCategoryView`         | Lists articles within a specific category.            | `articles_by_category`     |
| `subcategory/<slug:slug>/`   | `ArticlesBySubCategoryView`      | Lists articles within a specific subcategory.         | `articles_by_subcategory`  |
| `articles/trending/`         | `TrendingArticlesView`           | Displays articles marked as trending.                | `trending_articles`        |
| `articles/editors-pick/`     | `EditorsPickArticlesView`        | Displays articles flagged as editor's picks.         | `editors_pick_articles`    |
| `refresh-rss/`               | `refresh_rss_view`               | Triggers the RSS feed refresh to fetch new articles.  | `refresh_rss`              |

---

## **Project Structure**

### Accounts App
- **Purpose**: Manage user authentication, registration, and profile actions.  
- **Main Views**: 
  - `login_view`, `register_view`, `logout_view`
  - Class-based views: `UserProfileView`, `DeleteUserView`

### News App
- **Purpose**: Handle articles, categories, and news fetching.  
- **Main Views**: 
  - `HomePageView` for the homepage.  
  - `ArticleListView`, `ArticleDetailView` for article-related operations.  
  - `ArticlesByCategoryView`, `ArticlesBySubCategoryView` for category filtering.  
  - `TrendingArticlesView`, `EditorsPickArticlesView` for special filters.  
  - `refresh_rss_view` for RSS integration.

---

## **Future Enhancements**

- **Recommendation Engine**: Personalized news suggestions for users.  
- **Sentiment Analysis**: AI-driven insights on article tone.  
- **Admin Panel**: Simplified management of RSS feeds and article content.  
- **Breaking News Alerts**: Real-time notifications for trending topics.

---

## **Contributors**

- [Omofon](https://github.com/Omofon)

---

## **License**

This project is licensed under the [MIT License](LICENSE).
