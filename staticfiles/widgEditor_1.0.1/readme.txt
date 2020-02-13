*******************************************************************************
********************************* WIDGEDITOR **********************************
*******************************************************************************

CREATED BY:    Cameron Adams (http://www.themaninblue.com/)




License Information:
-------------------------------------------------------------------------------

Copyright (C) 2005 Cameron Adams

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA




Installation Instructions:
-------------------------------------------------------------------------------
In order to initialise widgEditor, place a script reference to "widgEditor.js"
in the head of the target HTML page. Any textareas with class="widgEditor"
will be automatically converted.

If you wish to use the default styles applied to the buttons, etc. you must
place a style reference to "widgEditor.css" in the head of the target HTML
page.




Browser Requirements:
-------------------------------------------------------------------------------
widgEditor uses the native editing capabilities contained in your browser.
At the moment this is only supported by Internet Exporer 5.5+ and Mozilla 1.3+.
Other browsers should receive the basic, unconverted textarea.

JavaScript must also be enabled to allow for widgEditor to initialise and
operate. Non-JavScript enabled browsers should receive the basic, unconverted
textarea.




Configuring widgEditor
-------------------------------------------------------------------------------
All simple configuration adjustments can be performed by modifying the config
variables at the head of the "widgEditor.js" file.

- The location of the widgEditor content CSS file. (How the editable content
  displays).

- Toolbar items to display.

- Block element formats to allow.

- Automatically insert paragraphs (recommended).

- Automatically clean pasted content (recommended).




Changing the interface
-------------------------------------------------------------------------------
All the visual elements of widgEditor are customisable using just the CSS file.

Edit "widgEditor.css" to style it how you want to, or just use the existing
CSS classes and build your own file.




Dynamically Created HTML Structure:
-------------------------------------------------------------------------------
Any replaced textareas are replaced by a series of dynamically created
elements.

To maintain uninterrupted form submission, the textarea's data submission is
replaced by a hidden input field of the same name and id. In addition to this,
several divs and an iframe are created to house the toolbar and the editing
pane.

Iframes are not XHTML 1.0+ compliant, so if you are being a real stickler,
widgEditor should only be used on HTML 4+ compliant pages. Internet Explorer
supports editing capabilities on non-document objects, such as divs, but
Mozilla currently only supports document objects, therefore an iframe must
be created to house the new document.

For a textarea id="editorX", the HTML structure of the dynamically created
elements would be:

<div id="editorXWidgContainer" class="widgContainer">
    <ul id="editorXWidgToolbar" class="widgToolbar">
        <li id="widgButtonBold" class="widgEditButton">
            <a></a>
        </li>
        .
        .
        .
        <li class="widgEditSelect">
            <select id="widgSelectBlock" name="widgSelectBlock">
            .
            .
            .
            </select>
        </li>
    </ul>
    <iframe id="editorXWidgIframe" class="widgIframe">
    </iframe>
<!--
     A textarea is swapped with the iframe when there is a need to
     view the HTML source
-->
    <textarea id="ORIGINAL_IDWidgTextarea" class="widgEditor">
    </textarea>
    <input id="editorX" name="editorX" type="hidden" />
    <input id="editorXWidgEditor" name="editorXWidgEditor" value="true" />
</div>




HTML Formatting
-------------------------------------------------------------------------------
widgEditor relies on the inbuilt HTML editors supplied with Internet Explorer
and Mozilla (no other browsers are known to support HTML editing embedded
on a web page). Therefore, much of the formatting and structure relies on
these native editors.

Some measure have been taken to ensure standards compliance, however when the
data is submitted from the form. Notably, Mozilla's editor produces far less
compliant code than Internet Explorer's.

Some of these measures include:

- Translation of inline styles (<span style="XXX">) to semantic tags <em> and
  <strong>.

- Translation of uppercase element tag names to lowercase.

- Quoting of element attributes.

- Removal of superfluous <br /> tags.




Backend Handling
-------------------------------------------------------------------------------
As with any public form element, the content arriving from widgEditor should
be checked for validity, etc.

You may wish to know whether the value submitted was via the plain textarea
or through a converted widgEditor. This can be deduced from the extra hidden
input -- noted above -- whose id/name is the original textarea's id/name with
"WidgEditor" appended. It submits a value of "true".