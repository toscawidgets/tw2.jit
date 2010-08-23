function setupTW2JitWidget(jitClassName, jitSecondaryClassName, attrs) {
    
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
        
    if ( jitSecondaryClassName ) {
        // Then use it!
        var jitwidget = new $jit[jitClassName][jitSecondaryClassName](attrs);
    } else {
        // Otherwise don't... I think only the 'TM' class
        //  has "secondary classes"
        var jitwidget = new $jit[jitClassName](attrs);
    }
    //jitwidget.loadJSON(data);
    
    return jitwidget;
}
