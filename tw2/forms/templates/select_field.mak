<%namespace name="tw" module="tw2.core.mako_util"/>\
<select ${tw.attrs(attrs=w.attrs)}>
    % for group, options in w.grouped_options:
     % if group is not None:
      <optgroup ${tw.attrs(attrs=dict(label=group))}>
     % endif 
        % for attrs, desc in options:
         <option ${tw.attrs(attrs=attrs)}>${desc}</option>
        % endfor
     % if group is not None:
      </optgroup>
     % endif 
    % endfor
</select>