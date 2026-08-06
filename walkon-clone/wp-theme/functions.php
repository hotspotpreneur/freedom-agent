<?php
/**
 * Kopite News Theme Functions
 */

// Register widget areas (for ads)
function kopite_news_widgets_init() {
    // Banner ad below header
    register_sidebar(array(
        'name'          => __('Banner Ad (Top)', 'kopite-news'),
        'id'            => 'banner-ad',
        'description'   => __('728x90 banner ad below header', 'kopite-news'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
    ));

    // Left sidebar ad
    register_sidebar(array(
        'name'          => __('Sidebar Ad (Left)', 'kopite-news'),
        'id'            => 'sidebar-ad-left',
        'description'   => __('160x600 ad in left sidebar', 'kopite-news'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
    ));

    // Right sidebar ad
    register_sidebar(array(
        'name'          => __('Sidebar Ad (Right)', 'kopite-news'),
        'id'            => 'sidebar-ad-right',
        'description'   => __('160x600 ad in right sidebar', 'kopite-news'),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
    ));
}
add_action('widgets_init', 'kopite_news_widgets_init');

// Theme setup
function kopite_news_setup() {
    // Add title tag support
    add_theme_support('title-tag');
    
    // Add custom logo support
    add_theme_support('custom-logo', array(
        'height'      => 100,
        'width'       => 400,
        'flex-height' => true,
        'flex-width'  => true,
    ));

    // Add featured image support
    add_theme_support('post-thumbnails');

    // Register navigation menu
    register_nav_menus(array(
        'primary' => __('Primary Menu', 'kopite-news'),
    ));
}
add_action('after_setup_theme', 'kopite_news_setup');

// Add custom meta box for article source
function kopite_news_add_source_metabox() {
    add_meta_box(
        'article_source',
        'Article Source',
        'kopite_news_source_callback',
        'post',
        'normal',
        'high'
    );
}
add_action('add_meta_boxes', 'kopite_news_add_source_metabox');

function kopite_news_source_callback($post) {
    $value = get_post_meta($post->ID, 'article_source', true);
    ?>
    <label for="article_source">Source Name: </label>
    <input type="text" id="article_source" name="article_source" value="<?php echo esc_attr($value); ?>" style="width: 100%;">
    <?php
}

function kopite_news_save_source($post_id) {
    if (array_key_exists('article_source', $_POST)) {
        update_post_meta($post_id, 'article_source', sanitize_text_field($_POST['article_source']));
    }
}
add_action('save_post', 'kopite_news_save_source');