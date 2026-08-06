</div><!-- #content -->

    <!-- Footer -->
    <footer id="colophon" class="site-footer">
        <div class="footer-content">
            <p class="copyright">
                &copy; <?php echo date('Y'); ?> <?php bloginfo('name'); ?>. All rights reserved.
            </p>
            <p class="footer-links">
                <a href="<?php echo esc_url(home_url('/')); ?>">Home</a> | 
                <a href="<?php echo get_permalink(get_option('page_for_posts')); ?>">News</a> |
                <a href="<?php echo esc_url(home_url('/contact')); ?>">Contact</a>
            </p>
        </div>
    </footer>

</div><!-- #page -->

<?php wp_footer(); ?>

</body>
</html>