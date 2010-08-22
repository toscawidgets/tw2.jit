function setupTW2JitWidget(
                jitwidget,
                jitClassName, attrs, data,
                preInitCallback, postInitCallback ) {

    if ( preInitCallback ) {
        preInitCallback(jitwidget);
    }

    jitwidget = new $jit[jitClassName](attrs);
    jitwidget.loadJSON(data);
    
    
    if ( postInitCallback ) {
        postInitCallback(jitwidget);
    }

    return jitwidget;
}
