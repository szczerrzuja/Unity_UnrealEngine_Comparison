using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MannequinScript : MonoBehaviour
{
    public Animator animator;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void SetAnimatorAnimation(int index, float animSpeed)
    {
        animator.SetFloat("AnimationSpeed", animSpeed);
        animator.SetInteger("AnimationID", index);
    }


}

