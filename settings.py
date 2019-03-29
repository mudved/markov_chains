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
                'all_pages_url_reg':r'(?<=dle-content)\s*.*?(?="navigation)',      #Список ссылок на все страницы 
                'pages_url_reg':r'(?<=href=")http.*?(?=" class="short)',           #Ссылка на страницу 
                'error_reg':r'(?<=div class="info">).*?(?=</div>)'                 #Страница не существует
                },
        'https://www.pornolomka.info':{
                'video_reg':r'(?<=:video" content=")\s*http.*?(?=")',
                'image_reg':r'(?<=:image" content=")\s*http.*?(?=")',
                'title_reg':r'(?<=title>)\s*.*?(?=<)',
                'description_reg':r'(?<=description" content=")\s*.*?(?=")',
                'h1_reg':r'(?<=news-title" itemprop="name">)\s*.*?(?=<)',
                'content_reg':r'(?<=itemprop="description">)\s*.*?(?=<)',
                'all_categories_reg':r'(?<=Категория:</b>).*(?=</div>)',
                'categories_reg':r'(?<=">).*?(?=</a>)',
                'all_tags_reg':r'(?<=Теги:</b>).*(?=</div>)',
                'tags_reg':r'(?<=">).*?(?=</a>)',
                'all_actors_reg':r'(?<=Актеры:</b>).*(?=</div>)',
                'actors_reg':r'(?<=">).*?(?=</a>)'
                }
        }
