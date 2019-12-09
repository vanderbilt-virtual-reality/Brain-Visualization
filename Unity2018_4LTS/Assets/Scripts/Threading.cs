using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Threading 
{
    private bool isDone = false;
    private object handle = new object();
    private System.Threading.Thread thread = null;

    public bool isCompleted()
    {
        return isDone;
    }

    public virtual void Start()
    {
        thread = new System.Threading.Thread(Run);
        thread.Start();
    }

    public virtual void Abort()
    {
        thread.Abort();
    }

    protected virtual void ThreadFunc() { }

    public virtual void OnFinished() { }

    public virtual string jobDescription() {
        return "";
    }

    public virtual bool Update()
    {
        if (isDone)
        {
            OnFinished();
            return true;
        }
        return false;
    }

    private void Run()
    {
        ThreadFunc();
        isDone = true;
    }
}
