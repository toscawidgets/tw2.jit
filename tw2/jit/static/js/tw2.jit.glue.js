function setupTW2JitWidget(jitClassName, jitSecondaryClassName, attrs) {
    if ( jitSecondaryClassName ) {
        return new $jit[jitClassName][jitSecondaryClassName](attrs);
    }
    return new $jit[jitClassName](attrs);
}
