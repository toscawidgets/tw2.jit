function setupTW2JitWidget(
                jitwidget,
                jitClassName, attrs, data,
                preInitCallback, postInitCallback ) {
    if ( preInitCallback ) {
        preInitCallback(jitwidget);
    }

    var jitwidget = new $jit[jitClassName](attrs);
    jitwidget.loadJSON(data);
    
    if ( postInitCallback ) {
        postInitCallback(jitwidget);
    }

    return jitwidget;
}
