{% macro get_vendor_data(vendor_col) %}

    {%
        set vendors = {
            1: 'Creative Mobile Technologies',
            2: 'VeriFone Inc.',
            4: 'Unknown/other'
        }
    %}

    case {{vendor_col}}
        {% for vendor_id, vendor_name in vendors.items() %}
            when {{vendor_id}} then '{{ vendor_name }}'
        {% endfor %}
    end

{% endmacro %}