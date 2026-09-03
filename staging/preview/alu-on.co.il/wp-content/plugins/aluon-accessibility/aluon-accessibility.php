<?php
/**
 * Plugin Name: Alu-on Accessibility Toolbar
 * Plugin URI: https://alu-on.co.il
 * Description: תוסף נגישות מקצועי ומקיף בתקן ת"י 5568 ו-WCAG 2.1 AA, הכולל סרגל נגישות צף, פאנל ניהול בתוך וורדפרס, שמירת הגדרות ב-LocalStorage, הקראת שינויים למיקוד ראייה ומגוון כלי התאמה אישית.
 * Version: 1.0.0
 * Author: האב מערכות מתקדמות בע"מ
 * Author URI: https://hub.co.il
 * Text Domain: aluon-a11y
 * Copyright: © 2026 האב מערכות מתקדמות בע"מ (Hub Advanced Systems Ltd.). כל הזכויות שמורות.
 * License: Proprietary. All Rights Reserved.
 */

if (!defined('ABSPATH')) {
    exit; // Exit if accessed directly
}

/* ==========================================================================
   Copyright (C) 2026 האב מערכות מתקדמות בע"מ
   כל הזכויות שמורות לחברת האב מערכות מתקדמות בע"מ.
   ========================================================================== */

class Aluon_Accessibility_Plugin {

    public function __construct() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_assets'));
        add_action('wp_footer', array($this, 'render_accessibility_markup'));
        add_action('admin_menu', array($this, 'add_admin_menu'));
        add_action('admin_init', array($this, 'register_settings'));
    }

    public function enqueue_assets() {
        if (get_option('aluon_a11y_enabled', '1') !== '1') {
            return;
        }

        wp_enqueue_style(
            'aluon-a11y-style',
            plugin_dir_url(__FILE__) . 'assets/css/accessibility.css',
            array(),
            '1.0.0'
        );

        wp_enqueue_script(
            'aluon-a11y-script',
            plugin_dir_url(__FILE__) . 'assets/js/accessibility.js',
            array(),
            '1.0.0',
            true
        );
    }

    public function render_accessibility_markup() {
        if (get_option('aluon_a11y_enabled', '1') !== '1') {
            return;
        }

        $pos = get_option('aluon_a11y_position', 'bottom-right');
        $color = get_option('aluon_a11y_color', '#0055ff');
        $statement_url = get_option('aluon_a11y_statement_url', '/accessibility/');
        ?>
        <!-- Alu-on Accessibility Plugin Markup (C) 2026 האב מערכות מתקדמות בע"מ -->
        <button id="aluonA11yBtn" class="aluon-a11y-btn aluon-pos-<?php echo esc_attr($pos); ?>" style="background:<?php echo esc_attr($color); ?>;" aria-label="תפריט נגישות מתקדם" title="תפריט נגישות">
            <i class="fa-solid fa-universal-access"></i>
        </button>

        <div id="aluonA11yPanel" class="aluon-a11y-panel aluon-pos-<?php echo esc_attr($pos); ?>" aria-label="אפשרויות נגישות" role="dialog" aria-modal="true" aria-hidden="true">
            <div class="aluon-a11y-header">
                <span><i class="fa-solid fa-universal-access"></i> תפריט נגישות</span>
                <button id="aluonA11yClose" class="aluon-a11y-close" aria-label="סגור תפריט נגישות"><i class="fa-solid fa-xmark"></i></button>
            </div>
            
            <div class="aluon-a11y-grid">
                <button class="aluon-a11y-opt" data-action="font-inc"><i class="fa-solid fa-text-height"></i> הגדלת טקסט</button>
                <button class="aluon-a11y-opt" data-action="font-dec"><i class="fa-solid fa-font"></i> הקטנת טקסט</button>
                <button class="aluon-a11y-opt" data-action="readable-font"><i class="fa-solid fa-glasses"></i> פונט קריא</button>
                <button class="aluon-a11y-opt" data-action="contrast"><i class="fa-solid fa-circle-half-stroke"></i> ניגודיות גבוהה</button>
                <button class="aluon-a11y-opt" data-action="invert"><i class="fa-solid fa-circle-nodes"></i> ניגודיות הפוכה</button>
                <button class="aluon-a11y-opt" data-action="grayscale"><i class="fa-solid fa-palette"></i> גווני אפור</button>
                <button class="aluon-a11y-opt" data-action="light-bg"><i class="fa-solid fa-sun"></i> רקע בהיר</button>
                <button class="aluon-a11y-opt" data-action="links"><i class="fa-solid fa-link"></i> הדגשת קישורים</button>
                <button class="aluon-a11y-opt" data-action="cursor"><i class="fa-solid fa-arrow-pointer"></i> סמן מוגדל</button>
                <button class="aluon-a11y-opt" data-action="stop-anim"><i class="fa-solid fa-hand"></i> עצירת תנועה</button>
            </div>

            <div class="aluon-a11y-footer">
                <a href="<?php echo esc_url($statement_url); ?>" class="aluon-a11y-opt aluon-a11y-link"><i class="fa-solid fa-file-contract"></i> הצהרת נגישות</a>
                <button class="aluon-a11y-opt aluon-a11y-reset" data-action="reset"><i class="fa-solid fa-rotate-left"></i> איפוס הגדרות</button>
            </div>
            
            <div style="font-size:0.68rem; color:#888899; text-align:center; margin-top:0.5rem; padding-top:0.4rem; border-top:1px solid rgba(255,255,255,0.08);">
                © 2026 האב מערכות מתקדמות בע"מ. כל הזכויות שמורות.
            </div>
        </div>

        <div id="aluonA11yLive" class="screen-reader-text" aria-live="polite" aria-atomic="true"></div>
        <?php
    }

    /* ==========================================================================
       WordPress Admin Panel Settings Page Integration
       ========================================================================== */
    public function add_admin_menu() {
        add_menu_page(
            'נגישות Alu-on',
            'נגישות Alu-on',
            'manage_options',
            'aluon-accessibility',
            array($this, 'render_admin_page'),
            'dashicons-universal-access',
            80
        );
    }

    public function register_settings() {
        register_setting('aluon_a11y_options_group', 'aluon_a11y_enabled');
        register_setting('aluon_a11y_options_group', 'aluon_a11y_position');
        register_setting('aluon_a11y_options_group', 'aluon_a11y_color');
        register_setting('aluon_a11y_options_group', 'aluon_a11y_statement_url');
    }

    public function render_admin_page() {
        ?>
        <div class="wrap" style="direction:rtl; font-family:'Rubik', sans-serif;">
            <h1 style="display:flex; align-items:center; gap:0.5rem;">
                <span class="dashicons dashicons-universal-access" style="font-size:2.2rem; width:auto; height:auto; color:#0055ff;"></span>
                סרגל נגישות Alu-on – ניהול והגדרות
            </h1>
            <p>פיתוח ובעלות בלעדית: <strong>האב מערכות מתקדמות בע"מ</strong> (תקן ת"י 5568 / WCAG 2.1 AA).</p>
            <hr />

            <form method="post" action="options.php" style="background:#fff; padding:2rem; border-radius:8px; border:1px solid #ccc; max-width:700px; margin-top:1.5rem;">
                <?php settings_fields('aluon_a11y_options_group'); ?>
                <?php do_settings_sections('aluon_a11y_options_group'); ?>

                <table class="form-table" style="width:100%;">
                    <tr>
                        <th scope="row">סטטוס תוסף נגישות</th>
                        <td>
                            <label>
                                <input type="checkbox" name="aluon_a11y_enabled" value="1" <?php checked(get_option('aluon_a11y_enabled', '1'), '1'); ?> />
                                הפעל סרגל נגישות צף באתר
                            </label>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">מיקום הכפתור הצף באתר</th>
                        <td>
                            <select name="aluon_a11y_position" style="padding:0.4rem; min-width:200px;">
                                <option value="bottom-right" <?php selected(get_option('aluon_a11y_position', 'bottom-right'), 'bottom-right'); ?>>ימין למטה (ברירת מחדל)</option>
                                <option value="bottom-left" <?php selected(get_option('aluon_a11y_position'), 'bottom-left'); ?>>שמאל למטה</option>
                                <option value="top-right" <?php selected(get_option('aluon_a11y_position'), 'top-right'); ?>>ימין למעלה</option>
                                <option value="top-left" <?php selected(get_option('aluon_a11y_position'), 'top-left'); ?>>שמאל למעלה</option>
                            </select>
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">צבע הכפתור הצף</th>
                        <td>
                            <input type="color" name="aluon_a11y_color" value="<?php echo esc_attr(get_option('aluon_a11y_color', '#0055ff')); ?>" />
                        </td>
                    </tr>
                    <tr>
                        <th scope="row">קישור לדף הצהרת נגישות</th>
                        <td>
                            <input type="text" name="aluon_a11y_statement_url" value="<?php echo esc_attr(get_option('aluon_a11y_statement_url', '/accessibility/')); ?>" class="regular-text" />
                        </td>
                    </tr>
                </table>

                <?php submit_button('שמור שינויים'); ?>
            </form>

            <div style="margin-top:2rem; color:#666; font-size:0.85rem;">
                © 2026 האב מערכות מתקדמות בע"מ. כל הזכויות שמורות. (Hub Advanced Systems Ltd.)
            </div>
        </div>
        <?php
    }
}

new Aluon_Accessibility_Plugin();
