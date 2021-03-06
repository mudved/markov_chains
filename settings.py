PARSING_PAGE_SETTINGS = {
        'http://pornolomka.me':{
                'video_reg':r'(?<=:video" content=")\s*http.*?(?=")',
                'image_reg':r'(?<=:image" content=")\s*http.*?(?=")',
                'title_reg':r'(?<=title>)\s*.*?(?=<)',
                'description_reg':r'(?<=description" content=")\s*.*?(?=")',
                'h1_reg':r'(?<=news-title" itemprop="name">)\s*.*?(?=<)',
                'content_reg':r'(?<=itemprop="description">)\s*.*?(?=<)',
                'all_categories_reg':r'(?<=Категория:</b>).*?(?=</div>)',
                'categories_reg':r'(?<=">).*?(?=</a>)',
                'all_tags_reg':r'(?<=Теги:</b>).*?(?=</div>)',
                'tags_reg':r'(?<=">).*?(?=</a>)',
                'all_actors_reg':r'(?<=Актеры:</b>).*?(?=</div>)',
                'actors_reg':r'(?<=">).*?(?=</a>)',
                'all_categories_url_reg':r'(?<=hidden_menu">)\s*.*?(?=</section)', #Список ссылок на все категории
                'categories_url_reg':r'(?<=href=").*?(?=">)',                      #Ссылка на категорию
                'template_cat_page_url':r'{cat_url}page/{i}/',                     #Шаблон url страницы категории
                'all_pages_url_reg':r'(?<=dle-content)\s*.*?(?="navigation)',      #Список ссылок на все страницы 
                'pages_url_reg':r'(?<=href=")http.*?(?=" class="short)',           #Ссылка на страницу 
                'error_reg':r'(?<=div class="info">).*?(?=</div>)'                 #Страница не существует
                },
        'https://www.pornolomka.info':{
                'video_reg':r'(?<=file:")http.*?(?=")',
                'image_reg':r'(?<=:image" content=")\s*http.*?(?=")',
                'title_reg':r'(?<=title>)\s*.*?(?=<)',
                'description_reg':r'(?<=description" content=")\s*.*?(?=")',
                'h1_reg':r'(?<=news-title" itemprop="name">)\s*.*?(?=<)',
                'content_reg':r'(?<=itemprop="description">).*?(?=<)',
                'all_categories_reg':r'(?<=Категория:</b>).*?(?=</div>)',
                'categories_reg':r'(?<=">).*?(?=</a>)',
                'all_tags_reg':r'(?<=Теги:</b>).*(?=</div>)',
                'tags_reg':r'(?<=">).*?(?=</a>)',
                'all_actors_reg':r'(?<=Актеры:</b>).*(?=</div>)',
                'actors_reg':r'(?<=">).*?(?=</a>)',
                'all_categories_url_reg':r'(?<=hidden_menu">)\s*.*?(?=</section)', #Список ссылок на все категории
                'categories_url_reg':r'(?<=href=").*?(?=">)',                      #Ссылка на категорию
                'template_cat_page_url':r'{cat_url}page/{i}/',                     #Шаблон url страницы категории
                'all_pages_url_reg':r'(?<=dle-content)\s*.*?(?="navigation)',      #Список ссылок на все страницы 
                'pages_url_reg':r'(?<=href=")http.*?(?=" class="short)',           #Ссылка на страницу 
                'error_reg':r'(?<=div class="info">).*?(?=</div>)'                 #Страница не существует
                },
        'http://krasivoe-porno.com':{
                'video_reg':r'(?<=file:")http.*?(?=")',
                'image_reg':r'(?<=:image" content=")\s*http.*?(?=")',
                'title_reg':r'(?<=title>)\s*.*?(?=<)',
                'description_reg':r'(?<=description" content=")\s*.*?(?=")',
                'h1_reg':r'(?<=news-title" itemprop="name">)\s*.*?(?=<)',
                'content_reg':r'(?<=itemprop="description">).*?(?=<)',
                'all_categories_reg':r'(?<=Категория:</b>).*?(?=</div>)',
                'categories_reg':r'(?<=">).*?(?=</a>)',
                'all_tags_reg':r'(?<=Теги:</b>).*(?=</div>)',
                'tags_reg':r'(?<=">).*?(?=</a>)',
                'all_actors_reg':r'(?<=Актеры:</b>).*(?=</div>)',
                'actors_reg':r'(?<=">).*?(?=</a>)',
                'all_categories_url_reg':r'(?<=hidden_menu">)\s*.*?(?=</section)', #Список ссылок на все категории
                'categories_url_reg':r'(?<=href=").*?(?=">)',                      #Ссылка на категорию
                'template_cat_page_url':r'{cat_url}page/{i}/',                     #Шаблон url страницы категории
                'all_pages_url_reg':r'(?<=dle-content)\s*.*?(?="navigation)',      #Список ссылок на все страницы 
                'pages_url_reg':r'(?<=href=")http.*?(?=" class="short)',           #Ссылка на страницу 
                'error_reg':r'(?<=div class="info">).*?(?=</div>)'                 #Страница не существует
                },
        'https://porno666.tv':{
                'video_reg':r'(?<=href=")https://porno666.tv/get.*?mp4(?=/\?download)',
                'image_reg':r'(?<=:image" content=")\s*http.*?(?=")',
                'title_reg':r'(?<=h1 class="">).*?(?=<)',
                'description_reg':r'(?<=description" content=")\s*.*?(?=")',
                'h1_reg':r'(?<=h1 class="">).*?(?=<)',
                'content_reg':r'(?<=<em>)\D\w+.*?(?=<)',
                'all_categories_reg':r'(?<=Категории:).*?(?=</div>)',
                'categories_reg':r'(?<=">).*?(?=</a>)',
                'all_tags_reg':r'(?<=Тэги:).*?(?=</div>)',
                'tags_reg':r'(?<=">).*?(?=</a>)',
                'all_actors_reg':r'(?<=Актеры:</b>).*(?=</div>)',
                'actors_reg':r'(?<=">).*?(?=</a>)',
                'all_categories_url_reg':r'(?<=ies_list_items">)\s*.*?(?="box tags-cloud")', #Список ссылок на все категории
                'categories_url_reg':r'(?<=a class="item" href=").*?(?=" title)',                      #Ссылка на категорию
                'template_cat_page_url':r'{cat_url}{i}/',                     #Шаблон url страницы категории
                'all_pages_url_reg':r'(?<=videos_list_items)\s*.*?(?="pagination)',      #Список ссылок на все страницы 
                'pages_url_reg':r'(?<=href=")http.*?(?=")',           #Ссылка на страницу 
                'error_reg':r'(?<=error">)404.*?(?=</div>)'                 #Страница не существует
                }
        }
