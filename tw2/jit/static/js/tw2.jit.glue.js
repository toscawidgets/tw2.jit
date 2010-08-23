function setupTW2JitWidget(
                jitClassName, jitSecondaryClassName,
                attrs, data,
                preInitCallback, postInitCallback ) {
    
    debug = true;
    if ( debug ) {
        console.log('------------');
        console.log(jitwidget);
        console.log(jitClassName);
        console.log(jitSecondaryClassName);
        console.log(attrs);
        console.log(data);
        console.log(preInitCallback);
        console.log(postInitCallback);
        console.log('------------');
    }
        

    if ( preInitCallback ) {
        preInitCallback();
    }

    console.log('pre...');
    if ( jitSecondaryClassName ) {
        // Then use it!
        var jitwidget = new $jit[jitClassName][jitSecondaryClassName](attrs);
    } else {
        // Otherwise don't... I think only the 'TM' class
        //  has "secondary classes"
        var jitwidget = new $jit[jitClassName](attrs);
    }
    console.log('pre-post');
    jitwidget.loadJSON(data);
    console.log('post...');
    
    
    if ( postInitCallback ) {
        postInitCallback(jitwidget);
    }

    return jitwidget;
}
