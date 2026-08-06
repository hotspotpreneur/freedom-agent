<?php get_header(); ?>

<div class="content-wrapper">
    <!-- Sidebar Ads - Left -->
    <aside class="sidebar-ads sidebar-left">
        <?php 
        if (is_active_sidebar('sidebar-ad-left')) {
            dynamic_sidebar('sidebar-ad-left');
        }
        ?>
    </aside>

    <div class="main-content">
        <?php while (have_posts()) : the_post(); ?>
            <article id="post-<?php the_ID(); ?>" <?php post_class('article-card'); ?>>
                <?php
                // Get category
                $categories = get_the_category();
                if (!empty($categories)) {
                    echo '<a href="' . esc_url(get_category_link($categories[0]->term_id)) . '" class="article-category">' . esc_html($categories[0]->name) . '</a>';
                }
                ?>
                
                <h1 class="article-title"><?php the_title(); ?></h1>
                
                <div class="article-meta">
                    <?php echo get_the_date(); ?> | 
                    <?php 
                    $source = get_post_meta(get_the_ID(), 'article_source', true);
                    if ($source) {
                        echo 'Source: ' . esc_html($source);
                    }
                    ?>
                </div>
                
                <div class="article-content">
                    <?php the_content(); ?>
                </div>
                
                <div class="article-tags">
                    <?php the_tags('<strong>Tags:</strong> ', ', '); ?>
                </div>
            </article>
            
            <!-- Post Navigation -->
            <div class="post-navigation">
                <?php 
                previous_post_link('%link', '&laquo; Previous Article');
                next_post_link('%link', 'Next Article &raquo;');
                ?>
            </div>
            
            <!-- Comments -->
            <?php 
            if (comments_open() || get_comments_number()) :
                comments_template();
            endif;
            ?>

        <?php endwhile; ?>
    </div>

    <!-- Sidebar Ads - Right -->
    <aside class="sidebar-ads sidebar-right">
        <?php 
        if (is_active_sidebar('sidebar-ad-right')) {
            dynamic_sidebar('sidebar-ad-right');
        }
        ?>
    </aside>
</div>

<?php get_footer(); ?>