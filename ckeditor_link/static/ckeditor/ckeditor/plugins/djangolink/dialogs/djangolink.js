
/**
 * @license Copyright (c) 2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

'use strict';

( function($) {
	CKEDITOR.dialog.add('djangolink', function( editor ) {
		var plugin = CKEDITOR.plugins.djangolink;
        var linkplugin = CKEDITOR.plugins.link;

		var commonLang = editor.lang.common,
			linkLang = editor.lang.link,
			anchors;

		return {
            'title': 'Link',
            'minWidth': 600,
            'minHeight': 330,
            'contents': [{
                'elements': [{
                    type: 'html',
                    html: '<iframe style="position:static; width:100%; height:100%; border:none;" />'
                }]
            }],
            'onOk': function () {
                // original link:804!
                var $iframe = $(CKEDITOR.dialog.getCurrent().parts.contents.$).find('iframe').contents();
                var $form = $iframe.find('form');
                var $fields = $form.find("input, select");
                var data = {};
                $.each($fields, function(index, field) {
                    var $field = $(field);
                    data[$field.attr("name")] = $field.val();
                });

				// TODO: submit data as ajax, if is_valid, get href from response, if not, check
				// errors in form

                var selection = editor.getSelection(),
					attributes = plugin.getLinkAttributes( editor, data );

				if ( !this._.selectedElement ) {
					var range = selection.getRanges()[ 0 ];

					// TODO: there is "link" as link text if none
					if ( range.collapsed ) {
                        var text = new CKEDITOR.dom.text('link', editor.document );
						range.insertNode(text);
						range.selectNodeContents(text);
					}

					// Apply style.
					var style = new CKEDITOR.style( {
						element: 'a',
						attributes: attributes.set
					} );

					style.type = CKEDITOR.STYLE_INLINE; // need to override... dunno why.
					style.applyToRange( range, editor );
					range.select();
				} else {
					// We're only editing an existing link, so just overwrite the attributes.
					var element = this._.selectedElement,
						href = element.data( 'cke-saved-href' ),
						textView = element.getHtml();

					element.setAttributes( attributes.set );
					element.removeAttributes( attributes.removed );

					// Update text view when user changes protocol (#4612).
					if ( href == textView || data.type == 'email' && textView.indexOf( '@' ) != -1 ) {
						// Short mailto link text view (#5736).
						element.setHtml( data.type == 'email' ?
							data.email.address : attributes.set[ 'data-cke-saved-href' ] );

						// We changed the content, so need to select it again.
						selection.selectElement( element );
					}

					delete this._.selectedElement;
				}

                // TODO: remove iframe??

                return true;
            },
			onShow: function() {
				var editor = this.getParentEditor(),
					selection = editor.getSelection(),
					element = null;

				// Fill in all the relevant fields if there's already one link selected.
				if ( ( element = plugin.getSelectedLink( editor ) ) && element.hasAttribute( 'href' ) ) {
					// Don't change selection if some element is already selected.
					// For example - don't destroy fake selection.
					if ( !selection.getSelectedElement() )
						selection.selectElement( element );
				} else {
					element = null;
				}

				// Record down the selected element in the dialog.
				this._.selectedElement = element;

				var data = plugin.parseLinkAttributes(element);
                var $iframe = $(CKEDITOR.dialog.getCurrent().parts.contents.$).find('iframe');
                $iframe.attr("src", editor.config.djangolinkIframeURL + "&" + $.param(data));
				$iframe.hide(0);
				var $dialog_content = $(CKEDITOR.dialog.getCurrent().parts.contents.$);
				$dialog_content.find('.cke_dialog_page_contents').css('height', '100%')
				$dialog_content.find('.cke_dialog_page_contents table[role=presentation]').css('height', '100%');

                $iframe.unbind('load');
                $iframe.bind('load', function () {
                    // tweak UI
					$iframe.show(0);
					var $iframe_content = $(this).contents();
                    $iframe_content.find('h1').hide().end();
                    $iframe_content.find('.submit-row').hide().end();
                    $iframe_content.find('#content').css('padding', 0);
                    $iframe_content.find('#container').css('min-width', 0).css('padding', 0);

                    // form
                    var $form = $(this).contents().find('form');
					$form.bind('submit', function(e) {
						e.preventDefault();
						// trigger onOK!?
					});

                });
			},
			onO22k: function() {
				var data = {};

				// Collect data from fields.
				this.commitContent( data );

				var selection = editor.getSelection(),
					attributes = plugin.getLinkAttributes( editor, data );

				if ( !this._.selectedElement ) {
					var range = selection.getRanges()[ 0 ];

					// Use link URL as text with a collapsed cursor.
					if ( range.collapsed ) {
						// Short mailto link text view (#5736).
						var text = new CKEDITOR.dom.text( data.type == 'email' ?
							data.email.address : attributes.set[ 'data-cke-saved-href' ], editor.document );
						range.insertNode( text );
						range.selectNodeContents( text );
					}

					// Apply style.
					var style = new CKEDITOR.style( {
						element: 'a',
						attributes: attributes.set
					} );

					style.type = CKEDITOR.STYLE_INLINE; // need to override... dunno why.
					style.applyToRange( range, editor );
					range.select();
				} else {
					// We're only editing an existing link, so just overwrite the attributes.
					var element = this._.selectedElement,
						href = element.data( 'cke-saved-href' ),
						textView = element.getHtml();

					element.setAttributes( attributes.set );
					element.removeAttributes( attributes.removed );

					// Update text view when user changes protocol (#4612).
					if ( href == textView || data.type == 'email' && textView.indexOf( '@' ) != -1 ) {
						// Short mailto link text view (#5736).
						element.setHtml( data.type == 'email' ?
							data.email.address : attributes.set[ 'data-cke-saved-href' ] );

						// We changed the content, so need to select it again.
						selection.selectElement( element );
					}

					delete this._.selectedElement;
				}



			},

		};

	} );

	CKEDITOR.tools.extend( CKEDITOR.config, {
		/**
		 * where to load the link iframe from
		 *
		 * @cfg {string} [djangolinkIframeURL='/admin/link/link/add']
		 * @member CKEDITOR.config
		 */
		djangolinkIframeURL: '/admin/link/link/add'

	} );

} )(django.jQuery);
