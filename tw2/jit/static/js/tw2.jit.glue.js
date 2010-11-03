

function setupTW2JitWidget(jitClassName, jitSecondaryClassName, id, attrs) {
    var w;
    if ( jitSecondaryClassName ) {
        w = new $jit[jitClassName][jitSecondaryClassName](attrs);
    } else {
        w = new $jit[jitClassName](attrs);
    }
    // Singleton:
    if ( window._jitwidgets === undefined ) {
        window._jitwidgets = {};
    }
    window._jitwidgets[id] = w;
    return w;
}
