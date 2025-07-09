# Vue.js Frontend Integration with Django Backend

This document outlines how to integrate Vue.js into the Django project to create a dynamic frontend that communicates with the Django backend API.

## Architecture Overview

The application will follow a hybrid approach:
- Django for server-side rendering of base templates
- Vue.js for dynamic frontend components
- Django REST Framework for API endpoints
- Vue components for interactive UI elements

## Setup Instructions

### 1. Install Vue.js Dependencies

Add these to your `requirements.txt` file for Django integration:
```
django-webpack-loader==1.7.0
```

Install Node.js and npm packages:
```bash
# Install Node.js and npm first if needed

# Create package.json
npm init -y

# Install Vue.js dependencies
npm install vue@3 vue-router@4 axios vuex@4 --save
npm install @vue/cli-service @vue/cli-plugin-babel @babel/preset-env babel-loader webpack webpack-cli webpack-bundle-tracker --save-dev
```

### 2. Project Structure for Vue.js Integration

Update your project structure to include Vue.js files:

```
mysite/
├── config/                  # Django project configuration
├── apps/                    # Django applications
├── templates/               # Django templates
├── static/                  # Static assets
├── media/                   # User uploaded content
├── frontend/                # Vue.js frontend code
│   ├── src/
│   │   ├── assets/          # Frontend assets
│   │   ├── components/      # Vue components
│   │   │   ├── profile/     # Profile components
│   │   │   ├── portfolio/   # Portfolio components
│   │   │   ├── blog/        # Blog components
│   │   │   └── contact/     # Contact form component
│   │   ├── views/           # Vue views
│   │   ├── router/          # Vue router configuration
│   │   ├── store/           # Vuex store modules
│   │   ├── api/             # API service modules
│   │   └── App.vue          # Root Vue component
│   ├── public/              # Public assets
│   ├── package.json         # Node dependencies
│   ├── vue.config.js        # Vue configuration
│   └── webpack.config.js    # Webpack configuration
└── manage.py                # Django management script
```

### 3. Configure Webpack for Vue.js

Create a `webpack.config.js` file in the frontend directory:

```javascript
// frontend/webpack.config.js
const path = require('path');
const BundleTracker = require('webpack-bundle-tracker');
const { VueLoaderPlugin } = require('vue-loader');

module.exports = {
  context: __dirname,
  entry: './src/main.js',
  output: {
    path: path.resolve('./static/vue/'),
    filename: '[name]-[hash].js',
    publicPath: '/static/vue/',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        }
      },
      {
        test: /\.vue$/,
        use: 'vue-loader',
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      }
    ]
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'}),
    new VueLoaderPlugin(),
  ],
  resolve: {
    extensions: ['.js', '.vue'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
    }
  },
};
```

### 4. Update Django Settings for Vue.js

Add webpack loader to your Django settings:

```python
# config/settings/base.py

INSTALLED_APPS += [
    'webpack_loader',
]

WEBPACK_LOADER = {
    'DEFAULT': {
        'CACHE': not DEBUG,
        'BUNDLE_DIR_NAME': 'vue/',  # must end with slash
        'STATS_FILE': os.path.join(BASE_DIR, 'frontend', 'webpack-stats.json'),
        'POLL_INTERVAL': 0.1,
        'TIMEOUT': None,
        'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
    }
}
```

### 5. Create Vue.js Entry Point

```javascript
// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// Configure axios for CSRF protection with Django
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

// Create Vue application
const app = createApp(App)

app.use(router)
app.use(store)

// Mount app to specific DOM elements
const elements = document.querySelectorAll('.vue-app')
elements.forEach(el => {
  // Clone the app instance for each mount point
  const clonedApp = app.mount(el)
})
```

### 6. Create Sample Vue Components

#### Profile Component
```vue
<!-- frontend/src/components/profile/ProfileInfo.vue -->
<template>
  <div class="profile-info" v-if="profile">
    <div class="text-xl-center">
      <h3 class="title title--h3 sidebar__name">{{ profile.name }}</h3>
      <div class="badge" v-for="badge in profile.badges" :key="badge.id">{{ badge.text }}</div>
    </div>
    
    <ul class="details-info" v-if="showContacts">
      <li class="details-info__item">
        <span class="box icon-box"><i class="font-icon icon-envelope"></i></span>
        <div class="contacts-block__info">
          <span class="overhead">Email</span>
          <a class="text-overflow" :href="`mailto:${profile.email}`">{{ profile.email }}</a>
        </div>
      </li>
      <li class="details-info__item">
        <span class="box icon-box"><i class="font-icon icon-phone"></i></span>
        <div class="contacts-block__info">
          <span class="overhead">Phone</span>
          <span class="text-overflow">{{ profile.phone }}</span>
        </div>
      </li>
      <!-- Other contact info -->
    </ul>
    
    <button class="btn btn--small btn--icon-right sidebar__btn" @click="toggleContacts">
      <span>{{ showContacts ? 'Hide Contacts' : 'Show Contacts' }}</span>
      <i class="feathericon-chevron-down"></i>
    </button>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'ProfileInfo',
  setup() {
    const profile = ref(null)
    const showContacts = ref(false)
    
    const fetchProfile = async () => {
      try {
        const response = await axios.get('/api/profiles/1/')
        profile.value = response.data
      } catch (error) {
        console.error('Error fetching profile:', error)
      }
    }
    
    const toggleContacts = () => {
      showContacts.value = !showContacts.value
    }
    
    onMounted(fetchProfile)
    
    return {
      profile,
      showContacts,
      toggleContacts
    }
  }
}
</script>
```

#### Contact Form Component
```vue
<!-- frontend/src/components/contact/ContactForm.vue -->
<template>
  <form class="contact-form" @submit.prevent="submitForm">
    <div class="row">
      <div class="form-group col-12 col-md-6">
        <input
          type="text"
          class="input form-control"
          v-model="form.fullName"
          placeholder="Full name"
          required
        >
        <div class="help-block with-errors"></div>
      </div>
      <div class="form-group col-12 col-md-6">
        <input
          type="email"
          class="input form-control"
          v-model="form.email"
          placeholder="Email address"
          required
        >
        <div class="help-block with-errors"></div>
      </div>
      <div class="form-group col-12 col-md-12">
        <textarea
          class="textarea form-control"
          v-model="form.message"
          placeholder="Your Message"
          rows="4"
          required
        ></textarea>
        <div class="help-block with-errors"></div>
      </div>
    </div>
    <div class="row">
      <div class="col-12 col-md-6 order-2 order-md-1 text-center text-md-start">
        <div id="validator-contact" class="hidden">{{ statusMessage }}</div>
      </div>
      <div class="col-12 col-md-6 order-1 order-md-2 text-end">
        <button type="submit" class="btn" :disabled="isSubmitting">
          <i class="font-icon icon-send"></i> Send Message
        </button>
      </div>
    </div>
  </form>
</template>

<script>
import { ref, reactive } from 'vue'
import axios from 'axios'

export default {
  name: 'ContactForm',
  setup() {
    const form = reactive({
      fullName: '',
      email: '',
      message: ''
    })
    
    const isSubmitting = ref(false)
    const statusMessage = ref('')
    
    const submitForm = async () => {
      isSubmitting.value = true
      statusMessage.value = ''
      
      try {
        const response = await axios.post('/api/contact/', {
          full_name: form.fullName,
          email: form.email,
          message: form.message
        })
        
        if (response.data.status === 'success') {
          statusMessage.value = 'Your message has been sent successfully!'
          form.fullName = ''
          form.email = ''
          form.message = ''
        } else {
          statusMessage.value = 'There was a problem sending your message. Please try again.'
        }
      } catch (error) {
        statusMessage.value = 'There was a problem sending your message. Please try again.'
        console.error('Error submitting form:', error)
      } finally {
        isSubmitting.value = false
      }
    }
    
    return {
      form,
      isSubmitting,
      statusMessage,
      submitForm
    }
  }
}
</script>
```

### 7. Update Django Templates to Use Vue Components

Modify your base Django templates to include Vue.js components:

```html
<!-- templates/base.html -->
{% load webpack_loader %}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mohammad Mahdi Samei{% endblock %}</title>
    {% include 'includes/meta.html' %}
    
    <!-- Styles -->
    <link rel="stylesheet" href="{% static 'styles/vendors/bootstrap.min.css' %}">
    <link rel="stylesheet" href="{% static 'styles/style.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <main class="main">
        <div class="container gutter-top gutter-bottom">
            <div class="row sticky-parent">
                <!-- Sidebar with Vue component -->
                <aside class="col-12 col-md-12 col-xl-3">
                    <div class="sidebar box-outer sticky-column vue-app" id="profile-sidebar">
                        <!-- Vue will mount here -->
                    </div>
                </aside>
                
                <!-- Content -->
                <div class="col-12 col-md-12 col-xl-9">
                    <div class="box-outer">
                        {% include 'includes/navigation.html' %}
                        {% block content %}{% endblock %}
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <div class="back-to-top"></div>
    
    <!-- JavaScripts -->
    <script src="{% static 'js/jquery-3.4.1.min.js' %}"></script>
    <script src="{% static 'js/plugins.min.js' %}"></script>
    <script src="{% static 'js/common.js' %}"></script>
    {% webpack_bundle 'main' %}
    {% block extra_js %}{% endblock %}
</body>
</html>
```

For the contact page:

```html
<!-- templates/contact.html -->
{% extends 'base.html' %}

{% block content %}
<div class="pb-0 pb-sm-2">
    <h1 class="title title--h1 title__separate">Contact</h1>
</div>

<!-- Contact -->
<div class="map" id="map"></div>
<h2 class="title title--h2">Contact Form</h2>

<!-- Vue Contact Form Component -->
<div class="vue-app" id="contact-form">
    <!-- Vue will mount here -->
</div>
{% endblock %}
```

### 8. API Integration

Create API services in Vue.js for communication with Django backend:

```javascript
// frontend/src/api/profile.js
import axios from 'axios'

export default {
  getProfile() {
    return axios.get('/api/profiles/1/') // Assuming there's only one profile
  },
  
  getSocialLinks() {
    return axios.get('/api/profiles/1/social-links/')
  }
}

// frontend/src/api/portfolio.js
import axios from 'axios'

export default {
  getProjects(category = null) {
    let url = '/api/projects/'
    if (category) {
      url += `?category=${category}`
    }
    return axios.get(url)
  },
  
  getProject(slug) {
    return axios.get(`/api/projects/${slug}/`)
  },
  
  getCategories() {
    return axios.get('/api/categories/')
  }
}

// frontend/src/api/contact.js
import axios from 'axios'

export default {
  sendMessage(data) {
    return axios.post('/api/contact/', data)
  }
}
```

### 9. State Management with Vuex

```javascript
// frontend/src/store/index.js
import { createStore } from 'vuex'
import profileModule from './modules/profile'
import portfolioModule from './modules/portfolio'
import blogModule from './modules/blog'

export default createStore({
  modules: {
    profile: profileModule,
    portfolio: portfolioModule,
    blog: blogModule
  }
})

// frontend/src/store/modules/profile.js
import profileApi from '@/api/profile'

export default {
  namespaced: true,
  
  state: () => ({
    profile: null,
    socialLinks: [],
    loading: false,
    error: null
  }),
  
  mutations: {
    SET_PROFILE(state, profile) {
      state.profile = profile
    },
    SET_SOCIAL_LINKS(state, links) {
      state.socialLinks = links
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async fetchProfile({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await profileApi.getProfile()
        commit('SET_PROFILE', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchSocialLinks({ commit }) {
      commit('SET_LOADING', true)
      try {
        const response = await profileApi.getSocialLinks()
        commit('SET_SOCIAL_LINKS', response.data)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    }
  },
  
  getters: {
    profileInfo: state => state.profile,
    socialLinks: state => state.socialLinks,
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    errorMessage: state => state.error
  }
}
```

### 10. Run Development Server

Update your package.json with scripts:

```json
{
  "scripts": {
    "serve": "vue-cli-service serve",
    "build": "vue-cli-service build",
    "watch": "vue-cli-service build --watch"
  }
}
```

Run Vue.js development server alongside Django:

```bash
# In one terminal (for Vue.js)
cd frontend
npm run watch

# In another terminal (for Django)
python manage.py runserver
```

## Key Benefits of Using Vue.js

1. **Reactive UI Components**: Vue's reactivity system automatically updates the UI when data changes
2. **Component-Based Architecture**: Modular, reusable components for each section of the site
3. **Smooth Transitions and Animations**: Vue provides built-in transition systems
4. **State Management**: Vuex for centralized state management
5. **API Integration**: Clean separation between frontend and backend with API services
6. **Performance Optimization**: Virtual DOM for efficient updates
7. **Improved User Experience**: Dynamic content loading without full page refreshes

## Integration Points with Django

1. **Authentication**: Use Django's authentication system with JWT tokens for Vue.js
2. **API Endpoints**: Django REST Framework provides API endpoints for Vue.js
3. **Initial Data Loading**: Server-side rendering for initial page load, then Vue.js takes over
4. **Form Validation**: Combine Django form validation with Vue.js frontend validation
5. **File Uploads**: Use Django to handle file uploads from Vue.js components
6. **SEO Optimization**: Server-side rendering for better SEO

## Production Deployment Considerations

1. **Static Asset Management**: Webpack bundles Vue.js components for production
2. **Code Splitting**: Lazy load Vue.js components for better performance
3. **Cache Control**: Proper headers for caching Vue.js bundles
4. **Error Handling**: Centralized error handling in both Django and Vue.js
5. **Monitoring**: Track frontend and backend performance separately

This approach gives you the best of both worlds: Django's robust backend capabilities with Vue.js's dynamic frontend features.
