/**
 Initial code from the ck editor default link plugin, by:
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

/*
 main things to do:
- main things done. working on nuances...and cleaning up!
  */


'use strict';

( function($) {
	CKEDITOR.plugins.add( 'djangolink', {
		requires: 'dialog,fakeobjects',
		// jscs:disable maximumLineLength
		// lang: 'af,ar,bg,bn,bs,ca,cs,cy,da,de,de-ch,el,en,en-au,en-ca,en-gb,eo,es,et,eu,fa,fi,fo,fr,fr-ca,gl,gu,he,hi,hr,hu,id,is,it,ja,ka,km,ko,ku,lt,lv,mk,mn,ms,nb,nl,no,pl,pt,pt-br,ro,ru,si,sk,sl,sq,sr,sr-latn,sv,th,tr,tt,ug,uk,vi,zh,zh-cn', // %REMOVE_LINE_CORE%
		// jscs:enable maximumLineLength
		icons: 'DjangoLink', // %REMOVE_LINE_CORE%
		hidpi: true, // %REMOVE_LINE_CORE%
		onLoad: function() {
			// Add the CSS styles for anchor placeholders.
			var iconPath = CKEDITOR.getUrl( this.path + 'images' + ( CKEDITOR.env.hidpi ? '/hidpi' : '' ) + '/anchor.png' ),
				baseStyle = 'background:url(' + iconPath + ') no-repeat %1 center;border:1px dotted #00f;background-size:16px;';

			var template = '.%2 a.cke_anchor,' +
				'.%2 a.cke_anchor_empty' +
				',.cke_editable.%2 a[name]' +
				',.cke_editable.%2 a[data-cke-saved-name]' +
				'{' +
					baseStyle +
					'padding-%1:18px;' +
					// Show the arrow cursor for the anchor image (FF at least).
					'cursor:auto;' +
				'}' +
				'.%2 img.cke_anchor' +
				'{' +
					baseStyle +
					'width:16px;' +
					'min-height:15px;' +
					// The default line-height on IE.
					'height:1.15em;' +
					// Opera works better with "middle" (even if not perfect)
					'vertical-align:text-bottom;' +
				'}';

			// Styles with contents direction awareness.
			function cssWithDir( dir ) {
				return template.replace( /%1/g, dir == 'rtl' ? 'right' : 'left' ).replace( /%2/g, 'cke_contents_' + dir );
			}

			CKEDITOR.addCss( cssWithDir( 'ltr' ) + cssWithDir( 'rtl' ) );
		},

		init: function( editor ) {
			var that = this;

			// mess with the original, remove link from context menu
			delete editor._.menuItems.link;

			var allowed = 'a[!href, data-*]',
				required = 'a[href]';

			editor.addCommand( 'djangolink', {
				allowedContent: allowed,
				requiredContent: required,
				exec: function () {
					var selection = editor.getSelection();
					var element = selection.getSelectedElement() || selection.getCommonAncestor().getAscendant('a', true);
					//var element = selection.getSelectedElement(); // || selection.getCommonAncestor().getAscendant('a', true);
					that.editLink(element, editor);
				}
			});


			if ( editor.ui.addButton ) {
				editor.ui.addButton( 'DjangoLink', {
					label: editor.lang.link.toolbar,
					command: 'djangolink',
					toolbar: 'djangolinks,10',
                    'icon': 'link'
				} );
			}

			CKEDITOR.dialog.add( 'djangolink', this.path + 'dialogs/djangolink.js' );

			editor.on( 'doubleclick', function( evt ) {
				var element = CKEDITOR.plugins.link.getSelectedLink( editor ) || evt.data.element;

				if ( !element.isReadOnly() ) {
					if ( element.is( 'a' ) ) {
						evt.data.dialog = ( element.getAttribute( 'name' ) && ( !element.getAttribute( 'href' ) || !element.getChildCount() ) ) ? 'anchor' : 'djangolink';

						// Pass the link to be selected along with event data.
						evt.data.link = element;
					} else if ( CKEDITOR.plugins.link.tryRestoreFakeAnchor( editor, element ) ) {
						evt.data.dialog = 'anchor';
					}
				}
			}, null, null, 0 );

			// If event was cancelled, link passed in event data will not be selected.
			editor.on( 'doubleclick', function( evt ) {
				// Make sure both links and anchors are selected (#11822).
				if ( evt.data.dialog in { djangolink: 1, anchor: 1 } && evt.data.link )
					editor.getSelection().selectElement( evt.data.link );
			}, null, null, 20 );

			// If the "menu" plugin is loaded, register the menu items.
			if ( editor.addMenuItems ) {
				editor.addMenuItems( {
					djangolink: {
						label: editor.lang.link.menu,
						'icon': 'link',
						command: 'djangolink',
						group: 'link',
						order: 1
					},
				} );
			}

			// If the "contextmenu" plugin is loaded, register the listeners.
			if ( editor.contextMenu ) {
				editor.contextMenu.addListener( function( element ) {
					if ( !element || element.isReadOnly() )
						return null;

					var anchor = CKEDITOR.plugins.link.tryRestoreFakeAnchor( editor, element );

					if ( !anchor && !( anchor = CKEDITOR.plugins.link.getSelectedLink( editor ) ) )
						return null;

					var menu = {};

					if ( anchor.getAttribute( 'href' ) && anchor.getChildCount() )
						menu = { djangolink: CKEDITOR.TRISTATE_OFF };

					return menu;
				} );
			}

		},

		 editLink:function(element, editor) {
			var $body = $('body');
            // var that = this;
			editor.openDialog('djangolink');
		},

		afterInit: function( editor ) {
			// Empty anchors upcasting to fake objects.
			editor.dataProcessor.dataFilter.addRules( {
				elements: {
					a: function( element ) {
						if ( !element.attributes.name )
							return null;

						if ( !element.children.length )
							return editor.createFakeParserElement( element, 'cke_anchor', 'anchor' );

						return null;
					}
				}
			} );

			var pathFilters = editor._.elementsPath && editor._.elementsPath.filters;
			if ( pathFilters ) {
				pathFilters.push( function( element, name ) {
					if ( name == 'a' ) {
						if ( CKEDITOR.plugins.link.tryRestoreFakeAnchor( editor, element ) || ( element.getAttribute( 'name' ) && ( !element.getAttribute( 'href' ) || !element.getChildCount() ) ) )
							return 'anchor';
					}
				} );
			}
		}
	} );

	function unescapeSingleQuote( str ) {
		return str.replace( /\\'/g, '\'' );
	}

	function escapeSingleQuote( str ) {
		return str.replace( /'/g, '\\$&' );
	}

	/**
	 * Set of Link plugin helpers.
	 *
	 * @class
	 * @singleton
	 */
	CKEDITOR.plugins.djangolink = {
		/**
		 * Get the surrounding link element of the current selection.
		 *
		 *		CKEDITOR.plugins.link.getSelectedLink( editor );
		 *
		 *		// The following selections will all return the link element.
		 *
		 *		<a href="#">li^nk</a>
		 *		<a href="#">[link]</a>
		 *		text[<a href="#">link]</a>
		 *		<a href="#">li[nk</a>]
		 *		[<b><a href="#">li]nk</a></b>]
		 *		[<a href="#"><b>li]nk</b></a>
		 *
		 * @since 3.2.1
		 * @param {CKEDITOR.editor} editor
		 */
		getSelectedLink: function( editor ) {
			var selection = editor.getSelection();
			var selectedElement = selection.getSelectedElement();
			if ( selectedElement && selectedElement.is( 'a' ) )
				return selectedElement;

			var range = selection.getRanges()[ 0 ];

			if ( range ) {
				range.shrink( CKEDITOR.SHRINK_TEXT );
				return editor.elementPath( range.getCommonAncestor() ).contains( 'a', 1 );
			}
			return null;
		},

		/**
		 * Collects anchors available in the editor (i.e. used by the Link plugin).
		 * Note that the scope of search is different for inline (the "global" document) and
		 * classic (`iframe`-based) editors (the "inner" document).
		 *
		 * @since 4.3.3
		 * @param {CKEDITOR.editor} editor
		 * @returns {CKEDITOR.dom.element[]} An array of anchor elements.
		 */
		getEditorAnchors: function( editor ) {
			var editable = editor.editable(),

				// The scope of search for anchors is the entire document for inline editors
				// and editor's editable for classic editor/divarea (#11359).
				scope = ( editable.isInline() && !editor.plugins.divarea ) ? editor.document : editable,

				links = scope.getElementsByTag( 'a' ),
				imgs = scope.getElementsByTag( 'img' ),
				anchors = [],
				i = 0,
				item;

			// Retrieve all anchors within the scope.
			while ( ( item = links.getItem( i++ ) ) ) {
				if ( item.data( 'cke-saved-name' ) || item.hasAttribute( 'name' ) ) {
					anchors.push( {
						name: item.data( 'cke-saved-name' ) || item.getAttribute( 'name' ),
						id: item.getAttribute( 'id' )
					} );
				}
			}
			// Retrieve all "fake anchors" within the scope.
			i = 0;

			while ( ( item = imgs.getItem( i++ ) ) ) {
				if ( ( item = this.tryRestoreFakeAnchor( editor, item ) ) ) {
					anchors.push( {
						name: item.getAttribute( 'name' ),
						id: item.getAttribute( 'id' )
					} );
				}
			}

			return anchors;
		},

		/**
		 * Opera and WebKit do not make it possible to select empty anchors. Fake
		 * elements must be used for them.
		 *
		 * @readonly
		 * @deprecated 4.3.3 It is set to `true` in every browser.
		 * @property {Boolean}
		 */
		fakeAnchor: true,

		/**
		 * For browsers that do not support CSS3 `a[name]:empty()`. Note that IE9 is included because of #7783.
		 *
		 * @readonly
		 * @deprecated 4.3.3 It is set to `false` in every browser.
		 * @property {Boolean} synAnchorSelector
		 */

		/**
		 * For browsers that have editing issues with an empty anchor.
		 *
		 * @readonly
		 * @deprecated 4.3.3 It is set to `false` in every browser.
		 * @property {Boolean} emptyAnchorFix
		 */

		/**
		 * Returns an element representing a real anchor restored from a fake anchor.
		 *
		 * @param {CKEDITOR.editor} editor
		 * @param {CKEDITOR.dom.element} element
		 * @returns {CKEDITOR.dom.element} Restored anchor element or nothing if the
		 * passed element was not a fake anchor.
		 */
		tryRestoreFakeAnchor: function( editor, element ) {
			if ( element && element.data( 'cke-real-element-type' ) && element.data( 'cke-real-element-type' ) == 'anchor' ) {
				var link = editor.restoreRealElement( element );
				if ( link.data( 'cke-saved-name' ) )
					return link;
			}
		},

		/**
		 * parses link attributes into data to be used by djangolink dialog
		 */
		parseLinkAttributes: function(editor, element ) {
			if (!element || !element.$.attributes) {
				return {};
			}
			var data = {};
			$.each(element.$.attributes, function(index, attribute) {
				var key = attribute.name.substr('data-'.length);
				// TODO: this mapping must go into a config!
				// TODO: this is probabla obsolete!
				if (key == "page_2") { key = "page"; }
				if (key == "page_1" || key == "page_3") { return; }
				data[key] = attribute.value;
			});
			// fallback: put href value into fallback field
			// for migrating legacy content
			if (!$(element).attr("data-ckeditor-link")) {
				if ($(element).attr("href")) {
					var key = editor.config.djangolinkFallbackField;
					data[key] = $(element).attr("href");
				}
			}
			return data
		},

		/**
		 * convert link data we get from an xhr (validated..) to actual data attributes.
		 */
		getLinkAttributes: function(editor, data, link_value) {
			var set = {}, removed;
			var excludes = ['_popup', '_save', 'csrfmiddlewaretoken'];

			$.each(data, function(index, item) {
				if ($.inArray(index, excludes) < 0) {
					if (item === null) {
						item = ''; // prevent attributes with "null" values!
					}
					set['data-' + index] = item;
				}
			});
			set['data-ckeditor-link'] = true;

			set.href = ''; // otherwise the a tag is removed from ck side.
			if (link_value) {
				set.href = link_value;
			}
			removed = [];

			return {
				set: set,
				removed: CKEDITOR.tools.objectKeys( removed )  // what?
			};
		}
	};

} )(django.jQuery);
