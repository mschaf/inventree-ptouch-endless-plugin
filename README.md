# inventree-ptouch-endless-plugin

A label printing plugin for [InvenTree](https://inventree.org), which provides additional support for Brother PTouch series printers.

## Notable Features
* Dynamic length labels, depending on the size of the content
* Pixel perfect rendering using a custom base template
* Automatic label width setting
* True length, the labels length will be nearly the requested template width (about ±0.5mm which is a hardware limitation)

## Template examples

### Basic example

The generated pdf will cover the printable of the label exactly, one px in css is a actual pixel on the label, enabling consistant 1px features like a 1px border.   
The `Height [mm]` from the template settings will determine the tape width (has to match what is in the machine) and the `Width [mm]` will determine its length. The printable area will be a bit smaller, as there the printers have a inherant margin on all sides.  

```
{% extends "label/ptouch_base.html" %}

{% block style %}
.border {
  width: {{ width_px }}px;
  height: {{ height_px }}px;
  border: 1px solid black;
  box-sizing: border-box;
}
{% endblock style %}

{% block content %}
<div class="border">
  Hello World!
</div>
{% endblock content %}
```

### Dynamic Width

By including `{% shrink_if_possible %}` in your `{% block content %}` the printer driver will cut of any whitespace to the right of the label, 
resulting in a label with a variable width depending on the content. The `Width [mm]` from the template settings is the max width in that scenario.

```
{% extends "label/ptouch_base.html" %}
{% load ptouch %}

{% block content %}
  {% shrink_if_possible %}
  Hello World!
{% endblock content %}
```


## Supported printers

The plugin is based on `labelprinterkit` which supports the following printers:

* P700
* P750W
* H500
* E500
* E550W

The plugin has only been tested with a `P750W`. 
The build in margins have been measured from labels printed by the `P750W`, if they dont fit other printers, provide me with better values through a issue or PR.
Other printers of the PTouch series might also work, but this is purly a suspicion.

### Minimum Requirements

This plugin now requires the InvenTree version `1.1.0` or newer.  
The plugin might function correctly on an InvenTree instance below version `1.1.0`, but this has not been tested.

### labelprinterkit

This plugin contains parts of https://github.com/ogelpre/labelprinterkit. Which could not be included via a dependency due to version conflicts. 