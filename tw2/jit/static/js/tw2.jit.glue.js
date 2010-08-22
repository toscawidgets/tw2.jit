function setupAnotherTW2JitWidget(
                jitClassName, attrs, data,
                preInitCallback, postInitCallback ) {
    if ( preInitCallback ) {
        preInitCallback();
    }

    var jitwidget = new $jit[jitClassName](attrs);
    jitwidget.loadJSON(data);
    jitwidget.refresh();

    if ( postInitCallback ) {
        postInitCallback();
    }
}
