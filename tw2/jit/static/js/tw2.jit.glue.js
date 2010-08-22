function setupTW2JitWidget(
                jitwidget,
                jitClassName, jitSecondaryClassName,
                attrs, data,
                preInitCallback, postInitCallback ) {

    if ( preInitCallback ) {
        preInitCallback(jitwidget);
    }

    if ( jitSecondaryClassName ) {
        // Then use it!
        console.log("using secondary: " + jitSecondaryClassName);
        jitwidget = new $jit[jitClassName][jitSecondaryClassName](attrs);
        console.log(jitwidget);
        console.log(jitwidget.type);
        console.log('foobar!!!');
    } else {
        // Otherwise don't... I think only the 'TM' class
        //  has "secondary classes"
        jitwidget = new $jit[jitClassName](attrs);
    }
    jitwidget.loadJSON(data);
    
    
    if ( postInitCallback ) {
        postInitCallback(jitwidget);
    }

    return jitwidget;
}
