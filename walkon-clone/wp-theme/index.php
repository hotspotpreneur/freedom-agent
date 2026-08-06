<?php get_header(); ?>

<div class="content-wrapper">
    <!-- Sidebar Ads - Left -->
    <aside class="sidebar-ads sidebar-left">
        <?php 
        if (is_active_sidebar('sidebar-ad-left')) {
            dynamic_sidebar('sidebar-ad-left');
        } else {
            echo '<div class="ad-sidebar">Advertisement</div>';
        }
        ?>
    </aside>

    <div class="main-content">
        <?php if (have_posts()) : ?>
            <div class="article-list">
                <?php while (have_posts()) : the_post(); ?>
                    <article id="post-<?php the_ID(); ?>" <?php post_class('article-card'); ?>>
                        <?php
                        // Get category
                        $categories = get_the_category();
                        if (!empty($categories)) {
                            echo '<a href="' . esc_url(get_category_link($categories[0]->term_id)) . '" class="article-category">' . esc_html($categories[0]->name) . '</a>';
                        }
                        ?>
                        
                        <h2 class="article-title">
                            <a href="<?php the_permalink(); ?>"><?php the_title(); ?></a>
                        </h2>
                        
                        <div class="article-meta">
                            <?php echo get_the_date(); ?>
                        </div>
                        
                        <div class="article-excerpt">
                            <?php the_excerpt(); ?>
                        </div>
                        
                        <div class="article-source">
                            Source: <?php 
                            $source = get_post_meta(get_the_ID(), 'article_source', true);
                            if ($source) {
                                echo esc_html($source);
                            } else {
                                bloginfo('name');
                            }
                            ?>
                        </div>
                    </article>
                <?php endwhile; ?>
            </div>

            <!-- Pagination -->
            <div class="pagination">
                <?php 
                the_posts_pagination(array(
                    'mid_size'  => 2,
                    'prev_text' => __('&laquo; Previous', 'kopite-news'),
                    'next_text' => __('Next &raquo;', 'kopite-news'),
                ));
                ?>
            </div>

        <?php else : ?>
            <p><?php _e('No articles found.', 'kopite-news'); ?></p>
        <?php endif; ?>
    </div>

    <!-- Sidebar Ads - Right -->
    <aside class="sidebar-ads sidebar-right">
        <?php 
        if (is_active_sidebar('sidebar-ad-right')) {
            dynamic_sidebar('sidebar-ad-right');
        } else {
            echo '<div class="ad-sidebar">Advertisement</div>';
        }
        ?>
    </aside>
</div>

<?php get_footer(); ?>