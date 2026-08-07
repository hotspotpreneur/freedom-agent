<?php get_header(); ?>

<div class="content-wrapper">
    <!-- Sidebar Ads - Left -->
    <aside class="sidebar-ads sidebar-left">
        <div class="ad-sidebar">Advertisement</div>
        <div class="ad-sidebar">Advertisement</div>
    </aside>

    <div class="main-content">
        <?php
        // Read the scraped news JSON (from theme folder)
        $json_path = dirname(__FILE__) . '/liverpool-news.json';
        $articles = array();
        $last_updated = '';
        
        if (file_exists($json_path)) {
            $json_data = file_get_contents($json_path);
            $data = json_decode($json_data, true);
            
            if ($data && isset($data['articles'])) {
                $articles = $data['articles'];
                $last_updated = isset($data['metadata']['last_updated']) ? $data['metadata']['last_updated'] : '';
            }
        }
        
        // If no articles from JSON, show a message
        if (empty($articles)) :
        ?>
            <div class="no-articles">
                <p>No articles available. Please run the scraper to fetch latest news.</p>
            </div>
        <?php else : ?>
            
            <!-- Featured Article (First one) -->
            <?php if (!empty($articles[0])) : ?>
            <div class="featured-article">
                <?php if (!empty($articles[0]['image'])) : ?>
                <a href="<?php echo esc_url($articles[0]['link']); ?>" target="_blank">
                    <img src="<?php echo esc_url($articles[0]['image']); ?>" alt="<?php echo esc_attr($articles[0]['title']); ?>">
                </a>
                <?php endif; ?>
                <div class="featured-content">
                    <?php if (!empty($articles[0]['category'])) : ?>
                    <span class="featured-category"><?php echo esc_html($articles[0]['category']); ?></span>
                    <?php endif; ?>
                    <h2 class="featured-title">
                        <a href="<?php echo esc_url($articles[0]['link']); ?>" target="_blank">
                            <?php echo esc_html($articles[0]['title']); ?>
                        </a>
                    </h2>
                    <?php if (!empty($articles[0]['summary'])) : ?>
                    <p class="featured-excerpt"><?php echo esc_html($articles[0]['summary']); ?></p>
                    <?php endif; ?>
                    <div class="article-meta">
                        <span class="source"><?php echo esc_html($articles[0]['source']); ?></span>
                        <?php if (!empty($articles[0]['date'])) : ?>
                        <span class="date"> - <?php echo esc_html($articles[0]['date']); ?></span>
                        <?php endif; ?>
                    </div>
                </div>
            </div>
            <?php endif; ?>
            
            <!-- Latest Update Time -->
            <?php if ($last_updated) : ?>
            <div class="last-updated">
                Last updated: <?php echo esc_html(date('F j, Y g:i a', strtotime($last_updated))); ?>
            </div>
            <?php endif; ?>
            
            <!-- Articles Grid -->
            <div class="article-list">
                <?php 
                // Skip first article (already shown as featured)
                $articles = array_slice($articles, 1);
                
                foreach ($articles as $article) : 
                ?>
                    <article class="article-card">
                        <?php if (!empty($article['image'])) : ?>
                        <div class="article-image">
                            <a href="<?php echo esc_url($article['link']); ?>" target="_blank">
                                <img src="<?php echo esc_url($article['image']); ?>" alt="<?php echo esc_attr($article['title']); ?>" loading="lazy">
                            </a>
                        </div>
                        <?php endif; ?>
                        
                        <div class="article-content">
                            <?php if (!empty($article['category'])) : ?>
                            <span class="article-category"><?php echo esc_html($article['category']); ?></span>
                            <?php endif; ?>
                            
                            <h3 class="article-title">
                                <a href="<?php echo esc_url($article['link']); ?>" target="_blank">
                                    <?php echo esc_html($article['title']); ?>
                                </a>
                            </h3>
                            
                            <?php if (!empty($article['summary'])) : ?>
                            <div class="article-excerpt">
                                <?php echo esc_html(mb_substr($article['summary'], 0, 150)); ?>...
                            </div>
                            <?php endif; ?>
                            
                            <div class="article-meta">
                                <span class="source"><?php echo esc_html($article['source']); ?></span>
                                <?php if (!empty($article['date'])) : ?>
                                <span class="date"> - <?php echo esc_html($article['date']); ?></span>
                                <?php endif; ?>
                                
                                <?php if (!empty($article['journalist'])) : ?>
                                <span class="journalist-tag"><?php echo esc_html($article['journalist']); ?></span>
                                <?php endif; ?>
                            </div>
                        </div>
                    </article>
                <?php endforeach; ?>
            </div>
            
        <?php endif; ?>
    </div>

    <!-- Sidebar Ads - Right -->
    <aside class="sidebar-ads sidebar-right">
        <div class="ad-sidebar">Advertisement</div>
        <div class="ad-sidebar">Advertisement</div>
        <div class="ad-sidebar">Advertisement</div>
    </aside>
</div>

<?php get_footer(); ?>