package com.renard.ocr.documents.creation;

import com.googlecode.tesseract.android.OCR;
import com.renard.ocr.MonitoredActivity;
import com.renard.ocr.R;
import com.renard.ocr.documents.creation.crop.CropImageActivity;
import com.renard.ocr.documents.creation.visualisation.OCRActivity;
import com.renard.ocr.documents.creation.NewDocumentActivity;
import com.renard.ocr.documents.viewing.DocumentContentProvider;
import com.renard.ocr.documents.viewing.DocumentContentProvider.Columns;
import com.renard.ocr.documents.viewing.grid.DocumentGridActivity;
import com.renard.ocr.documents.viewing.single.DocumentActivity;
import com.renard.ocr.pdf.Hocr2Pdf;
import com.renard.ocr.pdf.Hocr2Pdf.PDFProgressListener;
import com.renard.ocr.util.MemoryInfo;
import com.renard.ocr.util.Util;

import android.annotation.TargetApi;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.AlertDialog.Builder;
import android.app.Dialog;
import android.app.ProgressDialog;
import android.content.ActivityNotFoundException;
import android.content.BroadcastReceiver;
import android.content.ContentProviderClient;
import android.content.ContentValues;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.RemoteException;
import android.provider.MediaStore;
import android.support.v4.app.DialogFragment;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.content.FileProvider;
import android.support.v4.content.LocalBroadcastManager;
import android.support.v4.view.accessibility.AccessibilityManagerCompat;
import android.text.Html;
import android.text.Spanned;
import android.util.Base64;
import android.util.Log;
import android.util.Pair;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.accessibility.AccessibilityManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

import static com.renard.ocr.documents.creation.NewDocumentActivity.EXTRA_NATIVE_PIX;
import static com.renard.ocr.documents.creation.NewDocumentActivity.UPLOAD_IMAGE;
import com.googlecode.leptonica.android.WriteFile;
import com.googlecode.leptonica.android.Pix;
import java.lang.Object;

import com.android.volley.AuthFailureError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.sql.Timestamp;
import java.lang.Math;

/*  Created by: Shreyas Ambekar on
        April 1, 2020
    Modified by Hrishi Budhwant

* */

public class ImageUploadDialog extends Activity {

    int PICK_IMAGE_REQUEST = 111;
    String URL ="http://192.168.0.8:5000/file-upload";
    ProgressDialog progressDialog;

    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_imageupload);

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setMessage("Upload image?");
        builder.setTitle("Upload image?");
        builder.setNegativeButton("No", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Bundle extras = getIntent().getExtras();
                long nativePix = extras.getLong(EXTRA_NATIVE_PIX, 0);
                boolean accessibilityMode = extras.getBoolean(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, false);
                Intent result = new Intent();
                result.putExtra(UPLOAD_IMAGE, false);
                result.putExtra(EXTRA_NATIVE_PIX, nativePix);
                result.putExtra(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, accessibilityMode);
                setResult(RESULT_OK, result);
                finish();
            }
        });

        builder.setPositiveButton("Yes", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                Bundle extras = getIntent().getExtras();
                long nativePix = extras.getLong(EXTRA_NATIVE_PIX, 0);
                boolean accessibilityMode = extras.getBoolean(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, false);
                Pix mpix = new Pix(nativePix);
                Bitmap bitmap = WriteFile.writeBitmap(mpix);
                boolean download = false;

                progressDialog = new ProgressDialog(ImageUploadDialog.this);
                progressDialog.setMessage("Uploading, please wait...");
                progressDialog.show();

                //converting image to base64 string
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos);
                byte[] imageBytes = baos.toByteArray();
                final String imageString = Base64.encodeToString(imageBytes, Base64.DEFAULT);
                Timestamp timestamp = new Timestamp(System.currentTimeMillis());
                final String imgref = new String("IMG" + timestamp.getTime() + (Math.random() * 100));
                //  imgref = "IMG" + timestamp.getTime() + (Math.random() * 100);

                //sending image to server
                StringRequest request = new StringRequest(Request.Method.POST, URL, new Response.Listener<String>() {
                    @Override
                    public void onResponse(String s) {
                        progressDialog.dismiss();
                        if (s.equals("true")) {
                            Toast.makeText(ImageUploadDialog.this, "Uploaded Successful", Toast.LENGTH_LONG).show();

                        } else {
                            Toast.makeText(ImageUploadDialog.this, "Some error occurred!", Toast.LENGTH_LONG).show();
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError volleyError) {
                        Toast.makeText(ImageUploadDialog.this, "Some error occurred -> " + volleyError, Toast.LENGTH_LONG).show();
                    }
                }) {
                    //adding parameters to send
                    protected Map<String, String> getParams() throws AuthFailureError {
                        Map<String, String> parameters = new HashMap<String, String>();
                        //parameters.put("image", imageString);
                        parameters.put("image", imageString);
                        parameters.put("filename", imgref);
                        return parameters;
                    }
                };

                RequestQueue rQueue = Volley.newRequestQueue(ImageUploadDialog.this);
                rQueue.add(request);


                Intent result = new Intent();
                result.putExtra(UPLOAD_IMAGE, true);
                result.putExtra(EXTRA_NATIVE_PIX, nativePix);
                result.putExtra(OCRActivity.EXTRA_USE_ACCESSIBILITY_MODE, accessibilityMode);
                setResult(RESULT_OK, result);
                finish();
            }
        });
        AlertDialog alert = builder.create();
        alert.setCanceledOnTouchOutside(false);
        alert.show();
    }

    @Override
    public void onBackPressed() {
        super.onBackPressed();
        setResult(RESULT_CANCELED);
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

}