function A = dh_transform(theta, d, a, alpha)
% Standard Denavit-Hartenberg homogeneous transform.

    ct = cos(theta);
    st = sin(theta);
    ca = round(cos(alpha));
    sa = round(sin(alpha));

    A = [ct, -st*ca,  st*sa, a*ct;
         st,  ct*ca, -ct*sa, a*st;
          0,     sa,     ca,    d;
          0,      0,      0,    1];
end
