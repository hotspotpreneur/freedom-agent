<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <?php wp_head(); ?>
</head>

<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<div id="page" class="site">
    
    <!-- Header -->
    <header id="masthead" class="site-header">
        <div class="header-content">
            <?php if (get_header_image()) : ?>
                <div class="site-logo">
                    <a href="<?php echo esc_url(home_url('/')); ?>">
                        <img src="<?php header_image(); ?>" alt="<?php bloginfo('name'); ?>">
                    </a>
                </div>
            <?php else : ?>
                <h1 class="site-title">
                    <a href="<?php echo esc_url(home_url('/')); ?>"><?php bloginfo('name'); ?></a>
                </h1>
                <p class="site-description"><?php bloginfo('description'); ?></p>
            <?php endif; ?>
        </div>
    </header>

    <!-- Navigation -->
    <nav id="site-navigation" class="main-navigation">
        <?php
        wp_nav_menu(array(
            'theme_location' => 'primary',
            'menu_id'        => 'primary-menu',
            'fallback_cb'    => false,
        ));
        ?>
    </nav>

    <!-- Banner Ad - Below Header -->
    <div class="banner-ad-top">
        <?php 
        // AdSense placeholder - replace with your ad unit code
        if (is_active_sidebar('banner-ad')) {
            dynamic_sidebar('banner-ad');
        } else {
            echo '<span>Advertisement</span>';
        }
        ?>
    </div>

    <div id="content" class="site-content">